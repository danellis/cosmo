import unittest
from cosmo.database import Database

class DatabaseStoreRetrieveTest(unittest.TestCase):
    def setUp(self):
        self.database = Database(':memory:')

    def test(self):
        self.database.store_triples([
            ('http://example.com/start', 'page', 'http://example.com/absolute'),
            ('http://example.com/start', 'page', 'http://example.com/relative'),
            ('http://example.com/start', 'page', 'http://www.example.com/subdomain'),
            ('http://example.com/start', 'page', 'http://foo.example.net/otherdomain'),
            ('http://example.com/start', 'image', 'http://example.com/absimg'),
            ('http://example.com/start', 'image', 'http://example.com/relimg')
        ])

        triples = self.database.get_triples()
        self.assertIn(('http://example.com/start', 'page', 'http://example.com/absolute'), triples)
        self.assertIn(('http://example.com/start', 'page', 'http://example.com/relative'), triples)
        self.assertIn(('http://example.com/start', 'page', 'http://www.example.com/subdomain'), triples)
        self.assertIn(('http://example.com/start', 'page', 'http://foo.example.net/otherdomain'), triples)
        self.assertIn(('http://example.com/start', 'image', 'http://example.com/absimg'), triples)
        self.assertIn(('http://example.com/start', 'image', 'http://example.com/relimg'), triples)

class DatabaseFlushTest(unittest.TestCase):
    def test(self):
        database = Database(':memory:', flush=True)
        self.assertEqual(len(database.get_triples()), 0)

        database.store_triples([('a', 'b', 'c')])
        self.assertEqual(len(database.get_triples()), 1)

        database.flush()
        self.assertEqual(len(database.get_triples()), 0)
