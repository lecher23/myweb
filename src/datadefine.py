# coding: utf-8

from __future__ import unicode_literals, absolute_import
import time
import logging
from collections import namedtuple

Anchor = namedtuple('Anchor', ['owner', 'title', 'url', 'img', 'hot', 'comefrom'])


class BaseParser(object):
    def __init__(self, name, domain, web_pages):
        self.name = name
        self.domain = domain
        self.web_pages = web_pages
        self.anchors = []
        self.last_active = 0

    def _crawl(self, url):
        raise NotImplementedError('.')

    def crawl(self):
        try:
            self.anchors = []
            for page in self.web_pages:
                self._crawl(self.domain + page)
        except:
            logging.exception('crawl ')
        self.last_active = time.time()

    def out_of_date(self, effective_time=30):
        return time.time() - self.last_active <= effective_time

    def debug(self):
        s = []
        for anchor in self.anchors:
            s.append(anchor.owner)
            s.append(anchor.title)
            s.append(anchor.url)
            s.append(anchor.img)
            s.append(anchor.hot)
            s.append('---' * 10)
        print '\n'.join(s)

    @staticmethod
    def _convert_num(num):
        if num.endswith('万'):
            return int(float(num.replace('万', '').strip())) * 10000
        return int(num.strip())
