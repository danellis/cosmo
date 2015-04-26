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
            for _, link_type, link_url in triples:
                if link_type == 'page' and not self.database.is_page_stored(link_url):
                    self.queue.add(link_url)
