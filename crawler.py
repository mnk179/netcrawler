import requests
from collections import deque
from html.parser import HTMLParser

def determine_uri_scheme(uri):
    '''
    Determine the scheme of the URI
    The output can either be 'http', 'other', or ''
    '''
    scheme = uri[:16] # the longest id of an URI scheme is 15 characters
    if scheme[:4] == 'http':
        return 'http'
    elif scheme.find(':'):
        # we do not care of the exact scheme if it is not HTTP
        return 'other'
    else:
        return ''    

def handle_uri(uri):
    uri_scheme = determine_uri_scheme(uri)
    if uri_scheme == 'http':
        queue.appendleft(uri)
    elif uri_scheme == '':
        queue.appendleft(current_url + uri)

class LinkParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    handle_uri(attr[1])

link_parser = LinkParser()
url_set = set()
queue = deque()
start_url = 'https://news.ycombinator.com'
queue.appendleft(start_url)

while len(url_set) < 100:
    url = queue.pop()
    print('url', url)
    response = requests.get(url)

    current_url = response.url
    url_set.add(current_url)

    if response.status_code == 200:
        link_parser.feed(response.text)