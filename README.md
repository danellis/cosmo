# Cosmo

This is just a small, incomplete web crawler written as a coding test. Given a
starting URL, it will store link and image URLs per page in an SQLite database
as (page URL, link type, link URL) triples. The link types are `page` and
`image`. For a gathered link to be valid for crawling, it must:

* be of type 'page' (i.e. from the `href` of an `a` element)
* not have been crawled already
* have the same scheme, host and port as the page it was found on
* be permitted by robots.txt

```
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
```
