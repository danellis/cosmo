import requests

class Fetcher(object):
    def fetch(self, url):
        response = requests.get(url)
        return response.status_code, response.text
