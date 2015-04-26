from urllib.parse import urlparse

class Crawler(object):
    def __init__(self, database, fetcher, analyzer):
        self.database = database
        self.fetcher = fetcher
        self.analyzer = analyzer
        self.queue = set()

    def crawl(self, url):
        if self.database.is_page_stored(url):
            print("Page is already crawled. Use --flush to flush the database file.")
        else:
            self.queue.add(url)
            while len(self.queue) > 0:
                print("Queue size: {0}".format(len(self.queue)))
                self.crawl_one(self.queue.pop())

    def crawl_one(self, url):
        print("Crawling {0}".format(url))
        fetch_result = self.fetcher.fetch(url)
        if fetch_result is not None:
            (status, html) = fetch_result
            triples = self.analyzer.analyze(url, html)
            self.database.store_triples(triples)
            for page_url, link_type, link_url in triples:
                if self.should_crawl(page_url, link_type, link_url):
                    self.queue.add(link_url)

    def should_crawl(self, page_url, link_type, link_url):
        if not self.have_same_domain(page_url, link_url):
            return False

        if link_type == 'page' and self.database.is_page_stored(link_url):
            return False

        return True

    def have_same_domain(self, url1, url2):
        parsed1 = urlparse(url1)
        parsed2 = urlparse(url2)
        return (parsed1.scheme, parsed1.netloc) == (parsed2.scheme, parsed2.netloc)
