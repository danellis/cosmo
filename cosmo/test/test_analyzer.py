import unittest
from cosmo.analyzer import Analyzer

class AnalyzerTest(unittest.TestCase):
    def setUp(self):
        self.page_url = 'http://example.com/start'

        self.html = """
            <html><body>
                <a href="http://example.com/absolute"></a>
                <a href="relative"></a>
                <a href="http://www.example.com/subdomain"></a>
                <a href="http://foo.example.net/otherdomain"></a>
                <img src="http://example.com/absimg">
                <img src="relimg">
            </body></html>
        """

        analyzer = Analyzer()
        self.triples = analyzer.analyze(self.page_url, self.html)

    def test_absolute_link(self):
        self.assertIn((self.page_url, 'page', 'http://example.com/absolute'), self.triples)

    def test_relative_link(self):
        self.assertIn((self.page_url, 'page', 'http://example.com/relative'), self.triples)

    def test_subdomain_link(self):
        self.assertIn((self.page_url, 'page', 'http://www.example.com/subdomain'), self.triples)

    def test_otherdomain_link(self):
        self.assertIn((self.page_url, 'page', 'http://foo.example.net/otherdomain'), self.triples)

    def test_absolute_image(self):
        self.assertIn((self.page_url, 'image', 'http://example.com/absimg'), self.triples)

    def test_relative_image(self):
        self.assertIn((self.page_url, 'image', 'http://example.com/relimg'), self.triples)
