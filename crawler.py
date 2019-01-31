import requests
from collections import deque
from urllib.parse import urlparse, urljoin
from html.parser import HTMLParser

class LinkParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href' and self.limit > 0:
                    self.limit -= 1
                    self.data.append(attr[1])

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
    elif uri_scheme == '':
        url = urljoin(current_url, uri)
        if do_add(url_set, url):
            queue.appendleft(url)

def find_unique_urls(start_url, limit):
    """
    Find a set of size limit of unique URLs starting the crawl at start_url
    """
    link_parser = LinkParser()
    link_parser.data = []
    # we use are using a set since elements should be unique
    url_set = set()
    queue = deque()
    queue.appendleft(start_url)

    url_set.add(start_url)

    while len(url_set) < limit:
        # check if queue is empty
        if not queue:
            break
        url = queue.pop()
        print('url', url)
        link_parser.limit = limit
        response = requests.get(url)

        current_url = response.url
        
        if response.status_code == 200 and response.headers['content-type'][:9] == 'text/html':
            # find a way to use a generator
            link_parser.feed(response.text)
            for uri in link_parser.data:
                handle_uri(queue, url_set, current_url, uri)

    return url_set

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(find_unique_urls(str(sys.argv[1]), 100))