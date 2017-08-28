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

_null = object()


class BaseParser(object):
    def __init__(self, name, domain, web_pages):
        self.name = name
        self.domain = domain if domain.startswith('http') else ('http://' + domain)
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

    def _make_url(self, href):
        if href.startswith('/'):
            return self.domain + href
        return href

    def _extra_text(self, ele, path, default=_null):
        ''' ie:
        node1.(tag, attribute value).text
        node1.(tag, attribute value).[attribute name]
        '''
        nodes = path.split('.')
        for node in nodes[:-1]:
            if node.startswith('('):
                k, v = node[1:-1].split(',')
                ele = ele.find(k.strip(), v.strip())
            else:
                ele = getattr(ele, node, None)
            if not ele:
                if default == _null:
                    raise ValueError('get ele with node path {} from {} failed.'.format(node, ele))
                else:
                    return default
        if nodes[-1] == 'text':
            ret = getattr(ele, nodes[-1], default)
        else:
            ret = ele.get(nodes[-1].strip('[]'), default)
        if ret == _null:
            raise ValueError('get ele with {} from {} failed.'.format(path, ele))
        return ret.strip()

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
        print('\n'.join(s))

    @staticmethod
    def _convert_num(num):
        num = num.replace('人', '').replace(',', '')
        if num.endswith('万'):
            return int(float(num.replace('万', '').strip())) * 10000
        return int(num.strip())
