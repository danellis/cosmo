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
from cosmo import exit_codes

def main():
    # Process command line arguments
    arguments = docopt(__doc__, version=__version__)
    flush_db = arguments['--flush']
    output_raw = arguments['--raw']
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
        print_triples(database, raw=output_raw)
    except KeyboardInterrupt:
        print("Crawl terminated.", file=sys.stderr)
        print_triples(database, raw=output_raw)
    finally:
        # On completion, error or ^C, commit and close the DB cleanly
        database.close()

def print_triples(database, raw=False):
    triples = database.get_triples()

    if raw:
        print_raw_triples(triples)
    else:
        print_formatted_triples(triples)

def print_raw_triples(triples):
    for page_url, link_type, link_url in triples:
        print("{} {} {}".format(page_url, link_type, link_url))

def print_formatted_triples(triples):
    previous_page_url = None
    previous_link_type = None

    for page_url, link_type, link_url in triples:
        if page_url != previous_page_url:
            print(page_url)
            previous_page_url = page_url
        if link_type != previous_link_type:
            print("  Link type '{}':".format(link_type))
            previous_link_type = link_type
        print("    {}".format(link_url))

if __name__ == '__main__':
    main()
