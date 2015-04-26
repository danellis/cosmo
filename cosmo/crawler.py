import sys
from urllib.parse import urlparse, urlunparse
from urllib.robotparser import RobotFileParser

class Crawler(object):
    def __init__(self, database, fetcher, analyzer, verbose=False):
        self.database = database
        self.fetcher = fetcher
        self.analyzer = analyzer
        self.verbose = verbose
        self.queue = set()
        self.robot_parser = RobotFileParser()

    def crawl(self, url):
        if self.database.is_page_stored(url):
            print("Page is already crawled. Use --flush to flush the database file.", file=sys.stderr)
        else:
            self.load_robots_file(url)

            self.queue.add(url)
            while len(self.queue) > 0:
                self.crawl_one(self.queue.pop())

    def crawl_one(self, url):
        if self.verbose:
            print(url, file=sys.stderr)
        status, html = self.fetcher.fetch(url)
        triples = self.analyzer.analyze(url, html)
        self.database.store_triples(triples)
        for page_url, link_type, link_url in triples:
            if self.should_crawl(page_url, link_type, link_url):
                self.queue.add(link_url)

    def should_crawl(self, page_url, link_type, link_url):
        if link_type != 'page':
            return False

        if not self.have_same_domain(page_url, link_url):
            return False

        if not self.robot_parser.can_fetch('Cosmo', link_url):
            return False

        if self.database.is_page_stored(link_url):
            return False

        return True

    def have_same_domain(self, url1, url2):
        parsed1 = urlparse(url1)
        parsed2 = urlparse(url2)
        return (parsed1.scheme, parsed1.netloc) == (parsed2.scheme, parsed2.netloc)

    def load_robots_file(self, url):
        parsed = urlparse(url)
        robots_url = urlunparse((parsed.scheme, parsed.netloc, '/robots.txt', '', '', ''))
        self.robot_parser.set_url(robots_url)
        self.robot_parser.read()
