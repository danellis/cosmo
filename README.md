# Cosmo

***You have to run before you can crawl***

This is just a small, incomplete web crawler written as a coding test. Given a
starting URL, it will store link and image URLs per page in an SQLite database
as (page URL, link type, link URL) triples. The link types are `page`, `image`,
`stylesheet`, `script`, `object`, `embed`, `iframe`, `media` and `form`. For a
gathered link to be valid for crawling, it must:

* be of type `page` or `iframe`
* not have been crawled already
* have the same host and port as the page it was found on
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

## Known limitations

* There's no throttling
* Pages that fail to be retrieved are not retried
* Only HTML files are parsed, but it would be useful to parse CSS files too
* It's not at all concurrent
