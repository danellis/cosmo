"""Cosmo web crawler

Usage:
  cosmo [--database=<file>] [--flush] <url>
  cosmo -h|--help
  cosmo --version

Options:
  -h --help               Show this screen.
  --version               Show version.
  -d --database=<file>    Database file.
  -F --flush              Flush the database before crawling.
"""
__version__ = '0.0.1'

from docopt import docopt
from cosmo.database import Database
from cosmo.analyzer import Analyzer
from cosmo.fetcher import Fetcher
from cosmo.crawler import Crawler

def main():
    arguments = docopt(__doc__, version=__version__)
    flush_db = arguments['--flush']
    base_url = arguments['<url>']
    db_filename = arguments['--database'] or './cosmo.db'

    database = Database(db_filename, flush=flush_db)
    analyzer = Analyzer(database)
    fetcher = Fetcher()
    crawler = Crawler(fetcher, analyzer)
    crawler.crawl(base_url)

if __name__ == '__main__':
    main()
