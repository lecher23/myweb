# coding: utf-8

from __future__ import absolute_import, unicode_literals

import os
import sys
import json
import time
import signal
import logging
import tornado.gen
import tornado.ioloop
from tornado.web import Application
from tornado.options import options, define
from .handler import SimpleHandler
from .targets.common import CommonScanner

CUR = os.getcwd()


class ScannerFactory(object):
    def __init__(self, conf_path):
        obj = json.load(open(conf_path))
        self.scanners = [CommonScanner(k, v) for k, v in obj.items()]
        self.last_update = 0
        self.cache_time = 60
        self.anchors = []
        self.wake_interval = 120 * 1000
        self._timer = None

    def _expired(self):
        return time.time() - self.last_update > self.cache_time

    def start_timer_task(self):
        self._timer = tornado.ioloop.PeriodicCallback(self.update_async, self.wake_interval)
        self._timer.start()

    def stop_timer_task(self):
        self._timer.stop()

    def update(self):
        if self._expired():
            self.anchors = []
            for p in self.scanners:
                p.crawl()
                self.anchors += p.anchors
            self.last_update = time.time()

    @tornado.gen.coroutine
    def update_async(self):
        if self._expired():
            logging.info('begin async update')
            self.anchors = []
            for p in self.scanners:
                yield p.crawl_async()
                self.anchors += p.anchors
            self.last_update = time.time()


def register_signal(scanner_factory):
    def stop_server(signum, frame):
        logging.info('%s, %s', signum, frame)
        scanner_factory.stop_timer_task()
        tornado.ioloop.IOLoop.current().stop()

    signal.signal(signal.SIGQUIT, stop_server)
    signal.signal(signal.SIGINT, stop_server)
    signal.signal(signal.SIGTERM, stop_server)


def start_server(port):
    port = int(port)
    sf = ScannerFactory('conf/tv.json')
    sf.update()
    settings = {
        'static_path': os.path.join(CUR, 'views/static'),
        'static_url_prefix': 's',
        'debug': 'false',
        'template_path': os.path.join(CUR, 'views/dynamic'),
        'scanner': sf
    }

    app = Application(
        handlers=[(r'/', SimpleHandler)],
        **settings
    )

    app.listen(port)
    sf.start_timer_task()
    register_signal(sf)
    ioloop = tornado.ioloop.IOLoop.current()
    logging.info('server listen on port: %s', port)
    ioloop.start()


if __name__ == '__main__':
    define('port', default=9999, type=int, help='server port')
    sys.argv.append('--log_to_stderr=true')
    options.parse_command_line()
    start_server(options.port)
