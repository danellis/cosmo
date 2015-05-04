import unittest
from cosmo.crawler import Crawler

class CrawlerTest(unittest.TestCase):
    def setUp(self):
        self.crawler = Crawler(MockDatabase(), MockFetcher(), MockAnalyzer())
        self.crawler.robot_parser.allow_all = True
        self.crawler.crawl_one('http://example.com/start')

    def test(self):
        self.assertIn('http://example.com/absolute', self.crawler.queue)
        self.assertIn('http://example.com/relative', self.crawler.queue)
        self.assertNotIn('http://example.com/subdomain', self.crawler.queue)
        self.assertNotIn('http://example.com/otherdomain', self.crawler.queue)
        self.assertNotIn('http://example.com/absimg', self.crawler.queue)
        self.assertNotIn('http://example.com/relimg', self.crawler.queue)

class LinkTypeTest(unittest.TestCase):
    def setUp(self):
        self.crawler = Crawler(MockDatabase(), MockFetcher(), MockAnalyzer())
        self.crawler.robot_parser.allow_all = True

    def test(self):
        self.assertTrue(self.crawler.should_crawl('http://example.com/start', 'page', 'http://example.com/foo'))
        self.assertFalse(self.crawler.should_crawl('http://example.com/start', 'image', 'http://example.com/foo'))
        self.assertFalse(self.crawler.should_crawl('http://example.com/start', 'anything', 'http://example.com/foo'))

class SameDomainTest(unittest.TestCase):
    def setUp(self):
        self.crawler = Crawler(MockDatabase(), MockFetcher(), MockAnalyzer())
        self.crawler.robot_parser.allow_all = True

    def test(self):
        self.assertTrue(self.crawler.should_crawl('http://example.com/start', 'page', 'http://example.com/foo'))
        self.assertTrue(self.crawler.should_crawl('http://example.com/start', 'page', 'https://example.com/foo'))
        self.assertFalse(self.crawler.should_crawl('http://example.com/start', 'page', 'http://www.example.com/foo'))
        self.assertFalse(self.crawler.should_crawl('http://example.com/start', 'page', 'http://example.com:81/foo'))

class AlreadyCrawledTest(unittest.TestCase):
    def setUp(self):
        database = MockDatabase()
        self.crawler = Crawler(database, MockFetcher(), MockAnalyzer())
        self.crawler.robot_parser.allow_all = True
        database.store_triples([('http://example.com/foo', 'page', 'http://example.com/bar')])

    def test(self):
        self.assertFalse(self.crawler.should_crawl('http://example.com/start', 'page', 'http://example.com/foo'))
        self.assertTrue(self.crawler.should_crawl('http://example.com/start', 'page', 'http://example.com/bar'))

class RobotsTest(unittest.TestCase):
    def setUp(self):
        self.crawler = Crawler(MockDatabase(), RobotsFetcher(), MockAnalyzer())
        self.crawler.load_robots_file('http://example.com/start')

    def test(self):
        self.assertTrue(self.crawler.should_crawl('http://example.com/start', 'page', 'http://example.com/foo'))
        self.assertFalse(self.crawler.should_crawl('http://example.com/start', 'page', 'http://example.com/bar'))

class MockDatabase(object):
    def __init__(self):
        self.triples = []

    def close(self):
        pass

    def is_page_stored(self, page_url):
        for triple in self.triples:
            if triple[0] == page_url:
                return True
        return False

    def store_triples(self, triples):
        self.triples.extend(triples)

    def get_triples(self):
        return self.triples

class MockFetcher(object):
    def fetch(self, url):
        return 200, ''

class RobotsFetcher(object):
    def fetch(self, url):
        return (200,
"""User-Agent: *
Allow: /foo
Disallow: /bar
""")

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
