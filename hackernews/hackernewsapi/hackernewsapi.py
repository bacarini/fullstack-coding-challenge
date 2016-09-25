import requests

from .settings import *

session_request = requests.session()


class HackerNewsAPI(object):
    topstories_url = HACKERNEWS_API_TOPSTORIES or ''
    item_url = HACKERNEWS_API_ITEM or ''

    @staticmethod
    def do_get(url):
        response = session_request.get(url)
        response.raise_for_status()
        return response

    def get_ids_topstories(self, start=0, end=None):
        response = self.do_get(self.topstories_url)
        stories = response.json()[start:end]
        return stories

    def get_item_detail(self, item_id):
        url = self.item_url.format(item_id=item_id)
        response = self.do_get(url)
        return response.json()

    def get_comments_from_story(self, story_id):
        story = self.get_item_detail(story_id)
        comments_ids = story['kids']
        comments = self.get_comments(comments_ids)
        return comments

    def get_comments(self, comments_ids, deep=1, deeper=1):
        comments = []
        for comment_id in comments_ids:
            comment = self.get_item_detail(comment_id)
            if 'kids' in comment and deeper < deep:
                comment.update({'kids': self.get_comments(comment['kids'], deep, deeper)})
                comments.append(comment)
                deeper += 1
            else:
                comments.append(comment)
        return comments
