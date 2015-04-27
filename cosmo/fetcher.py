import requests
from cosmo.version import version

class Fetcher(object):
    """Helper class for performing HTTP GET operations."""

    headers = {
        'User-Agent': 'Cosmo/{}'.format(version)
    }

    def fetch(self, url):
        """Retrieve a resource from a URL.

        :param url: URL to retrieve.
        :returns: (status, text) or (None, None) if retrieval failed
        """
        try:
            response = requests.get(url, headers=self.headers)
            return response.status_code, response.text
        except requests.RequestException:
            return None, None
