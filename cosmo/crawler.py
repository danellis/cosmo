import sys
from urllib.parse import urlparse, urlunparse
from urllib.robotparser import RobotFileParser
import requests
from cosmo.version import version

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
        response = self.fetcher.fetch(url)
        if response is None:
            print("Failed to get {}".format(url), file=sys.stderr)
        else:
            status, html = response
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
        """Load the /robots.txt file for the given URL by reusing the scheme
        and authority parts.

        :param url: The URL from which to take the scheme and authority parts.
        :returns: None
        """
        parsed = urlparse(url)
        robots_url = urlunparse((parsed.scheme, parsed.netloc, '/robots.txt', '', '', ''))

        # Load the robots.txt file using the requests library, because we need
        # to specify the User-Agent header. I noticed on a CloudFlare-fronted
        # site that it returns a 403 for /robots.txt if the the user agent is
        # Python-urllib, but 200 if it's Cosmo.
        response = requests.get(robots_url, headers={'User-Agent': 'Cosmo/{}'.format(version)})
        if response.status_code in (401, 403):
            self.robot_parser.disallow_all = True
        elif response.status_code >= 400:
            self.robot_parser.allow_all = True
        else:
            self.robot_parser.parse(response.text)
