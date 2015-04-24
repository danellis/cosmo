from collections import deque

class Crawler(object):
    def __init__(self, fetcher, analyzer):
        self.fetcher = fetcher
        self.analyzer = analyzer
        self.queue = deque()

    def crawl(self, url):
        self.queue.append(url)
        while len(self.queue) > 0:
            print("Queue size: {0}".format(len(self.queue)))
            self.crawl_one(self.queue.popleft())

    def crawl_one(self, url):
        print("Crawling {0}".format(url))
        fetch_result = self.fetcher.fetch(url)
        if fetch_result is not None:
            (status, html) = fetch_result
            links = self.analyzer.analyze(url, html)
            for link in links:
                self.queue.append(link)
