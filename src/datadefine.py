# coding: utf-8

from __future__ import unicode_literals, absolute_import
import urllib3
urllib3.disable_warnings()
import time
import logging
import requests
from bs4 import BeautifulSoup
from collections import namedtuple

Anchor = namedtuple('Anchor', ['owner', 'title', 'url', 'img', 'hot', 'comefrom'])


class BaseParser(object):
    def __init__(self, name, domain, web_pages):
        self.name = name
        self.domain = domain
        self.web_pages = web_pages
        self.anchors = []
        self.last_active = 0

    def _crawl(self, page):
        r = requests.get(page, verify=False)
        doc = BeautifulSoup(r.content, 'html5lib')
        for anchor in self._extract_anchors(doc):
            try:
                ret = self._extract_anchor(anchor)
            except:
                logging.exception('get anchor from (%s) failed.', anchor)
            else:
                if ret:
                    self.anchors.append(ret)

    def _extract_anchors(self, doc):
        raise NotImplementedError('_extract_anchors')

    def _extract_anchor(self, anchor_doc):
        raise NotImplementedError('extract anchor')

    def crawl(self):
        try:
            self.anchors = []
            for page in self.web_pages:
                self._crawl(self.domain + page)
        except:
            logging.exception('crawl pages in (%s) failed.', self.web_pages)
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
