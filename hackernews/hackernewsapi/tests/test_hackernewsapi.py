from unittest import TestCase

from hackernewsapi.hackernewsapi import HackerNewsAPI


class HackerNewsTestCase(TestCase):

    def test_get_top_ten(self):
        stories = HackerNewsAPI().get_ids_topstories(start=0, end=10)
        self.assertEqual(len(stories), 10, u'The count is wrong, I was awaiting 10 items')

    def test_get_story_item_content(self):
        stories = HackerNewsAPI().get_ids_topstories(start=0, end=1)
        self.assertEqual(len(stories), 1, u'The count is wrong, I was awaiting 1 items')
        item = HackerNewsAPI().get_item_detail(stories[0])
        assertions_in = ['id', 'kids', 'title', 'type']
        for assertion in assertions_in:
            self.assertIn(assertion, item, u"The '{}' property not exists.".format(assertion))
        self.assertEqual(item['type'], 'story', u"The type is wrong, I was awaiting 'story'")

    def test_get_comments(self):
        stories = HackerNewsAPI().get_ids_topstories(start=0, end=1)
        item = HackerNewsAPI().get_item_detail(stories[0])
        comments = HackerNewsAPI().get_comments(item.get('kids'), deep=1)
        self.assertIn('id', comments[0])

