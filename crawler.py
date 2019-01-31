import requests
from collections import deque
from urllib.parse import urlparse, urljoin
from html.parser import HTMLParser
from bs4 import BeautifulSoup, SoupStrainer

def do_add(s, x):
    """
    Helper function that adds element to set and returns True if
    the value has been added, False if it has not
    """
    l = len(s)
    s.add(x)
    return len(s) != l

def handle_uri(queue, url_set, current_url, uri):
    """
    Handle discovered URIs: forms URLs if URI is a path only,
    rejects non-HTTP(S) URLs, adds valid URLs to the queue
    """
    uri_scheme = urlparse(uri).scheme
    if uri_scheme == 'http' or uri_scheme == 'https':
        url = uri
        # only add URL to queue if it is unique
        if do_add(url_set, url):
            queue.appendleft(url)
            return True
    elif uri_scheme == '':
        url = urljoin(current_url, uri)
        if do_add(url_set, url):
            queue.appendleft(url)
            return True
    return False

def find_unique_urls(start_url, limit):
    """
    Find a set of size limit of unique URLs starting the crawl at start_url
    """
    # we use are using a set since elements should be unique
    url_set = set()
    queue = deque()
    queue.appendleft(start_url)

    url_set.add(start_url)
    limit -= 1

    while len(url_set) < limit:
        # check if queue is empty
        if not queue:
            break
        url = queue.pop()
        response = requests.get(url)

        current_url = response.url
        
        if response.status_code == 200 and response.headers['content-type'][:9] == 'text/html':
            parse_only = SoupStrainer('a')
            soup = BeautifulSoup(response.text, "html.parser", parse_only=parse_only)
            for item in soup.children:
                if limit > 0:
                    if handle_uri(queue, url_set, current_url, item['href']):
                        limit -= 1

    return url_set

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(find_unique_urls(str(sys.argv[1]), 100))
    else:
        print('Please provide a starting url.')
        print('Use this to run:')
        print('python3 crawler.py \'https://www.mywebsite.com\'')
        print('or')
        print('python crawler.py \'https://www.mywebsite.com\'')
