# coding: utf-8

from __future__ import absolute_import, unicode_literals
from .targets.douyu import DouyuParser
from .targets.huya import HuyaParser
import time
import tornado.web


class ParserManager(object):
    def __init__(self):
        self.components = [
            DouyuParser(),
            HuyaParser()
        ]
        self.last_update = 0
        self.cache_time = 60
        self.anchors = []

    def update(self):
        if time.time() - self.last_update > self.cache_time:
            self.anchors = []
            for p in self.components:
                self.anchors += p.crawl()
            self.last_update = time.time()


class SimpleHandler(tornado.web.RequestHandler):
    _parsers_ = ParserManager()

    def get(self):
        self._parsers_.update()
        self.render('index.html', anchors=self._parsers_.anchors)
