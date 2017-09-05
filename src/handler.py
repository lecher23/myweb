# coding: utf-8

from __future__ import absolute_import, unicode_literals
import tornado.web


class SimpleHandler(tornado.web.RequestHandler):
    def get(self):
        scanner = self.settings['scanner']
        self.render('index.html', anchors=scanner.anchors)
