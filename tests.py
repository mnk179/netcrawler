import unittest
from crawler import find_unique_urls

class TestCrawler(unittest.TestCase):

    def setUp(self):
        self.start_url = 'https://www.netcraft.com'
        self.limit = 10
        self.url_set = find_unique_urls(self.start_url, self.limit)
        print('done setup')

    def test_set_size_matches_limit(self):
        self.assertEqual(len(self.url_set), self.limit)

    def test_set_contains_only_http_urls(self):
        for item in self.url_set:
            self.assertEqual(item[:4], 'http')

if __name__ == '__main__':
    unittest.main()