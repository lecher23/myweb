# coding: utf-8

from __future__ import absolute_import, unicode_literals
from .targets.douyu import DouyuParser
from .targets.huya import HuyaParser
import tornado.web


class SimpleHandler(tornado.web.RequestHandler):
    _douyu_ = DouyuParser()
    _huya_ = HuyaParser()

    def get(self):
        if self._douyu_.out_of_date():
            self._douyu_.crawl()
        if self._huya_.out_of_date():
            self._huya_.crawl()
        self.render('index.html', anchors=self._douyu_.anchors + self._huya_.anchors)
