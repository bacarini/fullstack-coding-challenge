import os

from werkzeug.test import Client
from unittest import TestCase
import hackernews
from tasks import do_request


class HackerNewsCloneTestCase(TestCase):

    def setUp(self):
        os.environ.setdefault('MONGO_DB', 'tests')
        hackernews.app.config['TESTING'] = True
        self.content = hackernews.app.app_context()

        self.client = Client(hackernews.app)

    def tearDown(self):
        pass

    def test_index(self):
        data, status, headers = self.client.get('/')
        body = data.next()
        self.assertEqual('200 OK', status)
        self.assertIn('No stories at this momment.', body,
                      "'No stories at this momment.' not found in Body Html.")

    def test_dorequest(self):
        url = 'https://httpbin.org'
        url_get = url + "/get?key=value"
        resp = do_request('GET', url_get,
                          headers={"Content-Type": 'application/json'})
        self.assertEqual(200, resp.status_code)
        self.assertEqual(resp.json().get('url'), url_get)
        self.assertEqual(resp.json().get('args', {}).get('key'), "value")

        url_post = url + "/post"
        resp = do_request('POST', url_post, data={"key": "value"},
                          headers={"Content-Type": 'application/json'})
        self.assertEqual(200, resp.status_code)
        self.assertEqual(resp.json().get('url'), url_post)
        self.assertEqual(resp.json().get('json', {}).get('key'), "value")

        url_patch = url + "/patch"
        resp = do_request('PATCH', url_patch, data={"key": "value"},
                          headers={"Content-Type": 'application/json'})
        self.assertEqual(200, resp.status_code)
        self.assertEqual(resp.json().get('url'), url_patch)
        self.assertEqual(resp.json().get('json', {}).get('key'), "value")

    def test_filters(self):
        trans = hackernews.trans_title
        mock = {"title_pt": "PT", "title_fr": "FR"}
        self.assertEqual(trans(mock, 'pt'), "PT")
        self.assertEqual(trans(mock, 'fr'), "FR")

        trans = hackernews.trans_status
        mock = {"unbabel_status_pt": "new", "unbabel_status_fr": "completed",
                "unbabel_uid_pt": "uidpt", "unbabel_uid_fr": "uidfr"}
        self.assertEqual(trans(mock, 'pt'), "uidpt/new")
        self.assertEqual(trans(mock, 'fr'), "uidfr/completed")