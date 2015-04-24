from urllib.request import urlopen
from urllib.error import HTTPError, URLError

class Fetcher(object):
    def fetch(self, url):
        try:
            response = (200, urlopen(url).read())
        except HTTPError as e:
            response = (e.code, '')
        except URLError:
            response = None
        return response
