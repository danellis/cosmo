from itertools import chain
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class Analyzer(object):
    def analyze(self, base_url, html):
        soup = BeautifulSoup(html)

        page_links = filter(None, map(self.map_tag(base_url, 'href'), soup.find_all('a')))
        image_links = filter(None, map(self.map_tag(base_url, 'src'), soup.find_all('img')))

        triples = chain(
            [(base_url, 'page', link_url) for link_url in page_links],
            [(base_url, 'image', link_url) for link_url in image_links]
        )

        return list(triples)

    def map_tag(self, base_url, url_attr):
        def _map_tag(tag):
            url = tag.attrs.get(url_attr, None)
            if url is None:
                return None
            else:
                return urljoin(base_url, url, allow_fragments=False)
        return _map_tag
