import threading
from random import choice
import queue
import requests
from urllib.parse import urljoin
from html.parser import HTMLParser
from time import sleep


class MyHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.links = []
        self.resources = []

    def handle_starttag(self, tag, attrs):
        dattrs = dict(attrs)
        if tag == 'a':
            self.links.append(dattrs.get('href', None))
        if tag in ('img', 'script'):
            self.resources.append(dattrs.get('src', None))
        if tag == 'link':
            self.links.append(dattrs.get('href', None))

        self.links = [link for link in self.links if link is not None]
        self.resources = [resource for resource in self.resources if resource is not None]

    def close(self):
        return (self.links, self.resources)


class SetQueue(queue.Queue):

    def _init(self, maxsize):
        self.queue = set()

    def _put(self, item):
        self.queue.add(item)

    def _get(self):
        return self.queue.pop()


class HTTP(threading.Thread):

    def __init__(self, config):
        threading.Thread.__init__(self)
        self.c = config
        self.q = SetQueue()
        self.start_page = choice(config['start-pages'].split())

    def _sanitize_url(self, page, url):
        if '//' in url:
            if url.startswith('//'):
                return 'http:' + url
            else:
                return url
        else:
            return urljoin(page, url)

    def _download_page(self, page):
        # Parse HTML
        html = requests.get(page).text
        p = MyHTMLParser()
        p.feed(html)
        links, resources = p.close()
        # Fill links to queue
        for link in links:
            print('saving link to queue - {}'.format(link))
            self.q.put(self._sanitize_url(page, link))

        # And download all resources of the page
        for resource in resources:
            print('downloading resource - {}'.format(resource))
            _ = requests.get(self._sanitize_url(page, resource)).text


    def run(self):
        print("starting on page {}".format(self.start_page))
        while True:
            if self.q.empty():
                page = self.start_page
            else:
                page = self.q.get()

            print('downloading data from {}'.format(page))
            self._download_page(page)

            sleep(int(self.c['delay']))
