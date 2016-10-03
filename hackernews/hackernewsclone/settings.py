# -*- coding: utf-8 -*-
import ConfigParser
from os.path import expanduser, join
home = expanduser("~")

config = ConfigParser.ConfigParser()
config.readfp(open(join(home, '.unbabel')))
UNBABEL_API_USERNAME = config.get('Sandbox', 'username')
UNBABEL_API_KEY = config.get('Sandbox', 'key')

UNBABEL_API_LANGUAGES = (
    ('en', u"English"),
    ('pt', u'Portuguese'),
    ('fr', u'French'),
)

HACKERNEWS_API_URL = 'https://hacker-news.firebaseio.com/v0'
HACKERNEWS_API_TOPSTORIES = '{}/topstories.json'.format(HACKERNEWS_API_URL)
HACKERNEWS_API_ITEM = '{}/item/{item_id}.json'.format(HACKERNEWS_API_URL, item_id='{item_id}')
