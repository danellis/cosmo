from urllib.parse import urljoin
from bs4 import BeautifulSoup

class Analyzer(object):
    def __init__(self, database):
        self.database = database

    def analyze(self, base_url, html):
        soup = BeautifulSoup(html)
        links = map(self.map_tag(base_url, 'href'), soup.find_all('a'))
        images = map(self.map_tag(base_url, 'src'), soup.find_all('img'))

        return filter(None, links)

    def map_tag(self, base_url, url_attr):
        def _map_tag(tag):
            url = tag.attrs.get(url_attr, None)
            if url is None:
                return None
            else:
                return urljoin(base_url, url, allow_fragments=False)
        return _map_tag
