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

import sys
from docopt import docopt
from cosmo.database import Database
from cosmo.analyzer import Analyzer
from cosmo.fetcher import Fetcher
from cosmo.crawler import Crawler
from cosmo import exit_codes

def main():
    # Process command line arguments
    arguments = docopt(__doc__, version=__version__)
    flush_db = arguments['--flush']
    base_url = arguments['<url>']
    db_filename = arguments['--database'] or './cosmo.db'

    # Open a database file for storing triples
    try:
        database = Database(db_filename, flush=flush_db)
    except Exception as e:
        print("Database error: {}", e)
        sys.exit(exit_codes.DATABASE)

    analyzer = Analyzer()
    fetcher = Fetcher()
    crawler = Crawler(database, fetcher, analyzer)

    try:
        # Start crawling from the supplied URL
        crawler.crawl(base_url)
    except KeyboardInterrupt:
        print("Crawl terminated.", file=sys.stderr)
    finally:
        # On error or ^C, commit and close the DB cleanly
        database.close()

if __name__ == '__main__':
    main()
