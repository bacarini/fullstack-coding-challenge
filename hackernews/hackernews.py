import time
from flask import Flask
from flask import render_template
from pymongo import MongoClient
from hackernewsapi.hackernewsapi import HackerNewsAPI

app = Flask(__name__)

mongo_client = MongoClient()
db = mongo_client.hackernewsclone


@app.route('/')
def index():
    stories = db.stories.find()
    return render_template('index.html', stories=stories)


@app.route('/comments/<story_id>')
def comments(story_id):
    story = db.stories.find_one({"id": int(story_id)})
    return render_template('comments.html', story=story)


@app.route('/fill')
def fill():
    stories = db.stories
    stories_ids = HackerNewsAPI().get_ids_topstories(0, 10)
    for story_id in stories_ids:
        story = HackerNewsAPI().get_item_detail(story_id)
        stories.insert_one(story)
    return "OK"


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.template_filter('ctime')
def timectime(s):
    return time.ctime(s)


if __name__ == '__main__':
    app.run()
