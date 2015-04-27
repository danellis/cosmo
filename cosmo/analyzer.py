from itertools import chain
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class Analyzer(object):
    def analyze(self, page_url, html):
        """Parse an HTML page and extract URLs from the links and images.

        :param page_url: The URL of the page being analyzed
        :param html:
        :return:
        """
        soup = BeautifulSoup(html)

        # Currently only `a` and `img` elements are used
        page_links = filter(None, map(self.map_tag(page_url, 'href'), soup.find_all('a')))
        image_links = filter(None, map(self.map_tag(page_url, 'src'), soup.find_all('img')))

        triples = chain(
            [(page_url, 'page', link_url) for link_url in page_links],
            [(page_url, 'image', link_url) for link_url in image_links]
        )

        # The list might be iterated over multiple times, so return it as a list
        return list(triples)

    def map_tag(self, page_url, url_attr):
        """Return a function that gets a URL the given attribute of an element.

        :param page_url: The URL of the page for making relative links absolute
        :param url_attr: The attribute to extract the URL from
        :returns: A function to map an element to a URL
        """
        def _map_tag(tag):
            url = tag.attrs.get(url_attr, None)
            if url is None:
                return None
            else:
                return urljoin(page_url, url, allow_fragments=False)
        return _map_tag
