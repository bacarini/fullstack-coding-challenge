# -*- coding:utf-8 -*-
import os
import requests
import errno

from celery.schedules import crontab
from celery.task import periodic_task
from requests import exceptions as requests_exceptions
from celery import Celery, chain, group
from retrying import retry
from httplib import BadStatusLine
from settings import HACKERNEWS_API_TOPSTORIES, HACKERNEWS_API_ITEM, UNBABEL_API_LANGUAGES
from hackernews import db

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')


celery = Celery('tasks',
                broker=CELERY_BROKER_URL,
                backend=CELERY_RESULT_BACKEND)


UNBABEL_HEADERS = {
            "Authorization": "ApiKey gtv.almeida:63215095a2bef30abea459ef841c681000c5d28d",
            "Content-Type": "application/json"
        }


def retry_if_resetpeer_or_timeout(exception):
    """Return True if we should retry (in this case when it's an these exceptions), False otherwise"""
    return not ((not isinstance(exception, requests_exceptions.ConnectionError)
                 and not isinstance(exception, requests_exceptions.ConnectTimeout))
                and not isinstance(exception, BadStatusLine or exception.errno == errno.ECONNRESET))


@retry(retry_on_exception=retry_if_resetpeer_or_timeout, wait_fixed=2000)
def do_request(method, url, data=None, headers=None):
    """
    A request with a method, posting the data value and using these headers
    :param method: POST or GET
    :param url:
    :param data:
    :param headers:
    :return:
    """
    try:
        if method == 'GET':
            resp = requests.get(url, headers=headers)
            return resp
        elif method == 'POST':
            resp = requests.post(url, json=data, headers=headers)
            return resp
        elif method == 'PATCH':
            resp = requests.patch(url, json=data, headers=headers)
            return resp
    except Exception, e:
        print "Retry {} with {}, {}".format(str(e), url, data)
        raise e


@celery.task(name='unbabel.post_unbabel_translation')
def post_unbabel_translation(item_id):
    """
    Send a post request to Unbabel API and return the responses if it's success.
    :param item_id:
    :return: response json from api
    """
    item = db.stories.find_one({"id": item_id})
    if item:
        response, objects = [], []
        for lang in [l[0] for l in UNBABEL_API_LANGUAGES if l[0] != 'en']:
            objects.append({"text": item.get('title'),  "target_language": lang, "text_format": "text"})
            data = {"objects": objects}
            resp = do_request('PATCH', "http://sandbox.unbabel.com/tapi/v2/translation/", data=data,
                              headers=UNBABEL_HEADERS)
            if resp.status_code == 202:
                data = resp.json()
                for object in data.get('objects', []):
                    db.stories.update_one({"_id": item.get('_id')},
                                          {"$set": {"unbabel_uid_{}".format(lang): object.get('uid')}})
                    response.append([resp.content, resp.json()])
        return response
    return "Item not found {}".format(item_id)


@celery.task(name='unbabel.get_unbabel_translations')
def get_unbabel_translation(uid, lang):
    """
    Make a request to Unbabel api to retrieve a translation detail.
    :return:
    """
    url = "http://sandbox.unbabel.com/tapi/v2/translation/{}/".format(uid)
    resp = do_request('GET', url, headers=UNBABEL_HEADERS)
    data = resp.json()

    update_data = {"$set": {"unbabel_status_{}".format(lang): data.get('status')}}
    if "completed" == data.get('status'):
        update_data.update({"$set": {"title_{}".format(lang): data.get('translatedText')}})
    db.stories.update_one({"id": uid}, update_data)
    return [{"id": uid}, update_data]


@periodic_task(run_every=crontab(minute='*/1'))
@celery.task(name='unbabel.handler_unbabel_translations')
def handler_unbabel_translations():
    """
    Run loop from stories and request a translation detail.
    :return:
    """
    jobs = []
    for item in db.stories.find({}):
        for lang in [l[0] for l in UNBABEL_API_LANGUAGES if l[0] != 'en']:
            uid = item.get('unbabel_uid_{}'.format(lang), None)
            if uid:
                jobs.append(get_unbabel_translation.s(uid, lang))
    job = group(jobs)
    job.apply_async()
    return job


@celery.task(name='hackernews.get_story_detail')
def save_story_detail(item_id):
    url = HACKERNEWS_API_ITEM.format(item_id=item_id)
    item_detail = do_request('GET', url).json()
    db.stories.insert_one(item_detail)
    return item_id


@periodic_task(run_every=crontab(minute='*/10'))
@celery.task(name='hackernews.update_topstories')
def update_topstories():
    db.stories.remove({})
    url = HACKERNEWS_API_TOPSTORIES
    stories_ids = do_request('GET', url).json()
    jobs = [chain(save_story_detail.s(sid), update_stories_comments.s(), post_unbabel_translation.s()) for sid in stories_ids[:10]]
    job = group(jobs)
    job.apply_async()
    return {"importing_stories": stories_ids}


@celery.task(name='hackernews.append_story_comment')
def append_story_comment(item_id):
    url = HACKERNEWS_API_ITEM.format(item_id=item_id)
    item_detail = do_request('GET', url).json()
    db.stories.update_one({"id": item_detail.get('parent')}, {"$push": {"comments": item_detail}})
    return item_detail



@celery.task(name='hackernews.update_stories_comments')
def update_stories_comments(item_id):
    item = db.stories.find_one({"id": item_id})
    jobs = []
    if item:
        for kid in item.get('kids', []):
            jobs.append(append_story_comment.s(kid))
        job = group(jobs)
        job.apply_async()
        return item_id
    return item_id
