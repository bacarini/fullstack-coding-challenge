# -*- coding: utf-8 -*-
UNBABEL_API_USERNAME = "gtv.almeida"
UNBABEL_API_KEY = "63215095a2bef30abea459ef841c681000c5d28d"

UNBABEL_API_LANGUAGES = (
    ('en', u"English"),
    ('pt', u'Portuguese'),
    ('fr', u'French'),
)

HACKERNEWS_API_URL = 'https://hacker-news.firebaseio.com/v0'
HACKERNEWS_API_TOPSTORIES = '{}/topstories.json'.format(HACKERNEWS_API_URL)
HACKERNEWS_API_ITEM = '{}/item/{item_id}.json'.format(HACKERNEWS_API_URL, item_id='{item_id}')
