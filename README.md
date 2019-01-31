# netcrawler

A simple web crawler implemented in Python.

Returns the first 100 unique URLs found after starting the crawl at the input URL. The program works in a breadth-first manner. It first records the unique URLs at the page being parsed currently. After all the links there have been exhausted, it fetches one of the URLs that it recorded previously.

**WARNING**: Do not use for anything serious. This crawler *does not* follow `robots.txt` conventions.

## Usage
To install, run:

```$ pip install -r requirements.txt```

To test, run:
```$ pip -m unittest```

To use, run:

```$ python crawler.py 'http://www.yourwebsite.com'```

Replace `'http://www.yourwebsite.com'` with the URL of the website you wish to start the crawl at.
