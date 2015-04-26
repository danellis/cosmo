"""Cosmo web crawler

Usage:
  cosmo [options] <url>
  cosmo -h|--help
  cosmo --version

Options:
  -h --help               Show this screen.
  --version               Show version.
  -v --verbose            Output each URL on stderr as it is fetched.
  -d --database=<file>    Database file.
  -F --flush              Flush the database before crawling.
  -f --format=<format>    Select output format (see below).

Output formats:
  nice      Hierarchical by page URL and link type
  raw       Raw triples
  dot       GraphViz DOT format graph
"""

import sys
from docopt import docopt
from cosmo.version import version
from cosmo.database import Database
from cosmo.analyzer import Analyzer
from cosmo.fetcher import Fetcher
from cosmo.crawler import Crawler
from cosmo.formatters import formatter_classes, default_format_name
from cosmo import exit_codes

def main():
    # Process command line arguments
    arguments = docopt(__doc__, version=version)
    verbose = arguments['--verbose']
    flush_db = arguments['--flush']
    base_url = arguments['<url>']
    db_filename = arguments['--database'] or './cosmo.db'
    format_name = arguments['--format'] or default_format_name

    formatter = get_formatter(format_name)

    # Open a database file for storing triples
    try:
        database = Database(db_filename, flush=flush_db)
    except Exception as e:
        print("Database error: {}", e)
        sys.exit(exit_codes.DATABASE)

    analyzer = Analyzer()
    fetcher = Fetcher()
    crawler = Crawler(database, fetcher, analyzer, verbose)

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

def get_formatter(format_name):
    format_class = formatter_classes.get(format_name)
    if format_class is None:
        print("Format '{}' not known.".format(format_name), file=sys.stderr)
        sys.exit(exit_codes.FORMAT)
    return format_class()

if __name__ == '__main__':
    main()
