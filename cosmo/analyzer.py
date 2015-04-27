from urllib.parse import urljoin
from bs4 import BeautifulSoup

class Analyzer(object):
    link_types = [
        # (link type, element, match attributes, extract attribute)
        ('page', 'a', {}, 'href'),
        ('image', 'img', {}, 'src'),
        ('stylesheet', 'link', {'rel': 'stylesheet'}, 'href'),
        ('script', 'script', {}, 'src'),
        ('object', 'object', {}, 'data'),
        ('embed', 'embed', {}, 'src'),
        ('iframe', 'iframe', {}, 'src'),
        ('media', 'source', {}, 'src'),
        ('form', 'form', {}, 'action')
    ]

    def analyze(self, page_url, html):
        """Parse an HTML page and extract URLs from the links and images.

        :param page_url: The URL of the page being analyzed
        :param html:
        :return:
        """
        soup = BeautifulSoup(html)

        triples = []
        for link_type, element_name, attrs, attribute_name in self.link_types:
            triples.extend(
                [
                    (page_url, link_type, self.extract_link(page_url, element, attribute_name))
                    for element
                    in soup.find_all(element_name, attrs=attrs)
                ]
            )

        return list(filter(lambda t: t[2] is not None, triples))

    def extract_link(self, page_url, element, attribute_name):
        """Return an absolute URL based on a base URL and a possibly relative one.

        :param page_url: URL of the page containing the link
        :param element: HTML element
        :param attribute_name: Attribute to extract the link from
        :returns: An absolute URL
        """
        attribute = element.attrs.get(attribute_name, None)
        if attribute is None:
            return None

        return urljoin(page_url, attribute, allow_fragments=False)
