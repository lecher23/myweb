# coding: utf-8

from __future__ import absolute_import, unicode_literals

import os
import sys
import json
import time
from .handler import SimpleHandler
from tornado.web import Application
from tornado.options import options, define
from .targets.common import CommonScanner
import tornado.ioloop

CUR = os.getcwd()


class ScannerFactory(object):
    def __init__(self, conf_path):
        obj = json.load(open(conf_path))
        self.scanners = [CommonScanner(k, v) for k, v in obj.items()]
        self.last_update = 0
        self.cache_time = 60
        self.anchors = []

    def update(self):
        if time.time() - self.last_update > self.cache_time:
            self.anchors = []
            for p in self.scanners:
                p.crawl()
                self.anchors += p.anchors
            self.last_update = time.time()


def start_server(port):
    settings = {
        'static_path': os.path.join(CUR, 'views/static'),
        'static_url_prefix': 's',
        'debug': 'true',
        'template_path': os.path.join(CUR, 'views/dynamic'),
        'scanner': ScannerFactory('conf/tv.json')
    }

    app = Application(
        handlers=[(r'/', SimpleHandler)],
        **settings
    )

    app.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    define('port', default=9999, type=int, help='server port')
    sys.argv.append('--log_to_stderr=true')
    options.parse_command_line()
    start_server(options.port)
