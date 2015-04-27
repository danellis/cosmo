import requests
from cosmo.version import version

class Fetcher(object):
    headers = {
        'User-Agent': 'Cosmo/{}'.format(version)
    }

    def fetch(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            return response.status_code, response.text
        except requests.RequestException:
            return None
