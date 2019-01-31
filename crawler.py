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

def handle_uri(queue, current_url, uri):
    '''
    Handles discovered URIs: forms URLs if URI is only the path,
    rejects non-HTTP(S) URLs, adds valid URLs to the queue
    '''
    uri_scheme = urlparse(uri).scheme
    if uri_scheme == 'http' or uri_scheme == 'https':
        queue.appendleft(uri)
    elif uri_scheme == '':
        queue.appendleft(urljoin(current_url, uri))

def find_unique_urls(start_url, limit):
    '''
    Main worker function
    '''
    link_parser = LinkParser()
    link_parser.data = []
    # we use are using a set since elements should be unique
    url_set = set()
    queue = deque()
    queue.appendleft(start_url)

    while len(url_set) < limit:
        # check if queue is empty
        if not queue:
            break
        url = queue.pop()
        link_parser.limit = limit
        response = requests.get(url)

        current_url = response.url
        url_set.add(current_url)

        if response.status_code == 200 and response.headers['content-type'][:9] == 'text/html':
            # find a way to use a generator
            link_parser.feed(response.text)
            for uri in link_parser.data:
                handle_uri(queue, current_url, uri)

    return url_set

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(find_unique_urls(str(sys.argv[1]), 20))