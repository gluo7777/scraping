# This script retrieves a list of free proxies

import requests
from bs4 import BeautifulSoup, Tag
import unittest


class ProxyClient:
    free_proxy_list_url = "https://free-proxy-list.net/"

    def __init__(self):
        pass

    def build_parser(self) -> BeautifulSoup:
        page_req = requests.get(ProxyClient.free_proxy_list_url)
        if page_req.status_code != 200:
            raise ConnectionError('Failed to retrieve page.')
        print("Retrieved %d bytes of data." % len(page_req.content))
        # load in bs
        return BeautifulSoup(page_req.text, 'lxml')

    def get_proxy_list(self) -> list:
        soup = self.build_parser()
        proxy_adresses = []
        row = soup.find('tr')
        while row is not None:
            data = row.findChildren('td')
            if len(data) == 8:
                proxy_adresses.append({
                    "address": data[0].getText(),
                    "port": data[1].getText(),
                    "country": data[3].getText(),
                    "https": data[6].getText() == "yes"
                })
            row = row.find_next('tr')
        print("Found %d valid proxies in list." % len(proxy_adresses))
        return proxy_adresses


class ProxyClientTest(unittest.TestCase):

    def test_get_proxy_list(self):
        client = ProxyClient()
        proxies = client.get_proxy_list()
        self.assertGreater(len(proxies), 0, "No proxies returned.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
