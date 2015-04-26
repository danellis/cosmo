"""Cosmo web crawler

Usage:
  cosmo [--database=<file>] [-F|--flush] [-r|--raw] <url>
  cosmo -h|--help
  cosmo --version

Options:
  -h --help               Show this screen.
  --version               Show version.
  -d --database=<file>    Database file.
  -F --flush              Flush the database before crawling.
  -r --raw                Output raw triples.
"""
__version__ = '0.0.1'

import sys
from docopt import docopt
from cosmo.database import Database
from cosmo.analyzer import Analyzer
from cosmo.fetcher import Fetcher
from cosmo.crawler import Crawler
from cosmo.format.nice import NiceFormatter
from cosmo.format.raw import RawFormatter
from cosmo import exit_codes

def main():
    # Process command line arguments
    arguments = docopt(__doc__, version=__version__)
    flush_db = arguments['--flush']
    base_url = arguments['<url>']
    db_filename = arguments['--database'] or './cosmo.db'

    if arguments['--raw']:
        formatter = RawFormatter()
    else:
        formatter = NiceFormatter()

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
        formatter.print(database.get_triples())
    except KeyboardInterrupt:
        print("Crawl terminated.", file=sys.stderr)
        formatter.print(database.get_triples())
        sys.exit(exit_codes.SUCCESS)
    except Exception as e:
        print("Error: {}".format(e), file=sys.stderr)
        sys.exit(exit_codes.ERROR)
    finally:
        database.close()

if __name__ == '__main__':
    main()
