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
        """Begin recursively crawling pages starting from the given URL.

        :param url: Starting URL
        :returns: None
        """
        if self.database.is_page_stored(url):
            print("Page is already crawled. Use --flush to flush the database file.", file=sys.stderr)
        else:
            # Because crawling is restricted to pages on the same domain, the
            # robots.txt file can be loaded once at the beginning of the crawl
            self.load_robots_file(url)

            # Add the starting URL to the queue of pages to be crawled, and
            # then keep crawling while there are still URLs in the queue
            self.queue.add(url)
            while len(self.queue) > 0:
                self.crawl_one(self.queue.pop())

    def crawl_one(self, url):
        """Fetch a single page and analyze it for links. The found triples are
        stored in the database, and found links that should be crawled are
        added to the queue.

        :param url: The page to fetch and analyze
        :returns: None
        """
        if self.verbose:
            print(url, file=sys.stderr)

        status, html = self.fetcher.fetch(url)

        if status is None:
            # The status code will be None if retrieval failed
            print("Failed to get {}".format(url), file=sys.stderr)
        else:
            # Search for links and images in the page, and get them as triples
            # of (page URL, link type, link URL)
            triples = self.analyzer.analyze(url, html)

            self.database.store_triples(triples)

            # Any linked URLs that are eligible for crawling are added to the
            # pending crawl queue
            for page_url, link_type, link_url in triples:
                if self.should_crawl(page_url, link_type, link_url):
                    self.queue.add(link_url)

    def should_crawl(self, page_url, link_type, link_url):
        """Determine whether a URL should be crawled.

        :param page_url: The page the link came from.
        :param link_type: The type of link URL.
        :param link_url: The link URL to test.
        :returns: True if the link URL should be crawled, otherwise False.
        """
        # Only linked pages should be crawled, not images
        if link_type != 'page':
            return False

        # The link should be on the same domain as the page it's linked from
        if not self.have_same_domain(page_url, link_url):
            return False

        # Fetching the link URL should be permitted by robots.txt
        if not self.robot_parser.can_fetch('Cosmo', link_url):
            return False

        # The linked page should not have been crawled already
        if self.database.is_page_stored(link_url):
            return False

        return True

    def have_same_domain(self, url1, url2):
        """Test whether two URLs have the same hostname and port.

        :returns: True if they do, otherwise False
        """
        return urlparse(url1).netloc == urlparse(url2).netloc

    def load_robots_file(self, url):
        """Load the /robots.txt file for the given URL by reusing the scheme
        and authority parts.

        :param url: The URL from which to take the scheme and authority parts.
        :returns: None
        """
        # Create a new URL with the same scheme, host and port, but with a
        # path of /robots.txt
        parsed = urlparse(url)
        robots_url = urlunparse((parsed.scheme, parsed.netloc, '/robots.txt', '', '', ''))

        # Load the robots.txt file using the requests library, because we need
        # to specify the User-Agent header. I noticed on a CloudFlare-fronted
        # site that it returns a 403 for /robots.txt if the the user agent is
        # Python-urllib, but 200 if it's Cosmo.
        status, robots_file = self.fetcher.fetch(robots_url)
        if status in (401, 403):
            self.robot_parser.disallow_all = True
        elif status >= 400:
            self.robot_parser.allow_all = True
        else:
            self.robot_parser.parse(robots_file.splitlines())
