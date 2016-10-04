# -*- coding: utf-8 -*-
import time
import os
from worker import celery
import celery.states as states
from flask import Flask, render_template, url_for
from pymongo import MongoClient, DESCENDING
from settings import UNBABEL_API_LANGUAGES

app = Flask(__name__)
mongo_host = os.getenv('MONGO_HOST') or '127.0.0.1'
mongo_client = MongoClient(host=mongo_host)

db = mongo_client.hackernewsclone


@app.route('/')
@app.route('/<lang>')
def index(lang='en'):
    languages = UNBABEL_API_LANGUAGES
    stories = db.stories.find({}).sort("score", DESCENDING)
    return render_template('index.html', stories=stories, languages=languages, lang=lang)


@app.route('/<lang>/comments/<int:story_id>')
def comments(story_id, lang='en'):
    story = db.stories.find_one({"id": story_id})
    return render_template('comments.html', story=story, lang=lang)


@app.route('/dashboard')
def dashboard():
    languages = UNBABEL_API_LANGUAGES[1:]
    stories = db.stories.find()
    return render_template('dashboard.html', stories=stories, languages=languages)


@app.route('/fill')
def fill():
    task = celery.send_task('hackernews.update_topstories', args=[], kwargs={})
    return "<a href='{url}'>check status of {id} </a>".format(obj_id=task.id,
                                                              url=url_for('check_task', id=task.id, _external=True))


@app.route('/clear')
def clear():
    stories = db.stories
    stories.delete_many({})
    return "OK"


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.template_filter('ctime')
def timectime(s):
    return time.ctime(s)


@app.template_filter('trans_title')
def trans_title(obj, lang):
    if lang == 'en':
        return obj.get("title")
    title = obj.get("title_"+lang)
    return title or u"{} <small>(not translated)</small>".format(obj.get("title"))


@app.template_filter('trans_status')
def trans_status(obj, lang):
    uid = obj.get('unbabel_uid_{}'.format(lang.lower()))
    status = obj.get('unbabel_status_{}'.format(lang.lower()))
    if status:
        status = "/{}".format(status)
    return "{}{}".format(uid, status)


@app.route('/check/<string:obj_id>')
def check_task(obj_id):
    res = celery.AsyncResult(obj_id)
    if res.state == states.PENDING:
        return res.state
    else:
        return str(res.result)


@app.route('/get_translations')
def get_translations():
    task = celery.send_task('unbabel.get_unbabel_translation', args=[], kwargs={})
    return "<a href='{url}'>check status of {id} </a>".format(id=task.id, url=url_for('check_task', id=task.id,
                                                                                      _external=True))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
