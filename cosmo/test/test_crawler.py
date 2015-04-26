import unittest
from cosmo.crawler import Crawler

class CrawlerTest(unittest.TestCase):
    def setUp(self):
        self.crawler = Crawler(MockDatabase(), MockFetcher(), MockAnalyzer())
        self.crawler.crawl_one('http://example.com/start')

    def test_queue(self):
        self.assertIn('http://example.com/absolute', self.crawler.queue)
        self.assertIn('http://example.com/relative', self.crawler.queue)
        self.assertNotIn('http://example.com/subdomain', self.crawler.queue)
        self.assertNotIn('http://example.com/otherdomain', self.crawler.queue)
        self.assertNotIn('http://example.com/absimg', self.crawler.queue)
        self.assertNotIn('http://example.com/relimg', self.crawler.queue)

class MockDatabase(object):
    def __init__(self):
        self.triples = []

    def close(self):
        pass

    def is_page_stored(self, page_url):
        return False

    def store_triples(self, triples):
        self.triples.extend(triples)

    def get_triples(self):
        return self.triples

class MockFetcher(object):
    def fetch(self, url):
        return 200, ''

class MockAnalyzer(object):
    def analyze(self, page_url, html):
        return [
            (page_url, 'page', 'http://example.com/absolute'),
            (page_url, 'page', 'http://example.com/relative'),
            (page_url, 'page', 'http://www.example.com/subdomain'),
            (page_url, 'page', 'http://foo.example.net/otherdomain'),
            (page_url, 'image', 'http://example.com/absimg'),
            (page_url, 'image', 'http://example.com/relimg')
        ]
