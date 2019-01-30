import requests
from collections import deque
from html.parser import HTMLParser

def handle_url(url):
    url_set.add(url)
    queue.appendleft(url)

class LinkParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    handle_url(attr[1])

link_parser = LinkParser()
url_set = set()
queue = deque()
start_url = 'https://news.ycombinator.com'
queue.appendleft(start_url)

while len(url_set) < 100:
    url = queue.pop()

    response = requests.get(url)

    if response.status_code == 200:
        link_parser.feed(response.text)