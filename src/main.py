# coding: utf-8

from __future__ import absolute_import, unicode_literals

import os
import sys
import json
import signal
import logging
import tornado.gen
import tornado.ioloop
from tornado.web import Application
from tornado.options import options, define
from .handler import SimpleHandler,JjHandler
from .targets.common import CommonScanner

CUR = os.getcwd()


class ScannerFactory(object):
    def __init__(self, conf_path):
        obj = json.load(open(conf_path))
        self.scanners = [CommonScanner(k, v) for k, v in obj.items()]
        self.cache_time = 60
        self.anchors = []
        self.wake_interval = 10
        self._timer = None

    def start_update_job(self):
        tornado.ioloop.IOLoop.current().spawn_callback(self.update_async)

    @tornado.gen.coroutine
    def update_async(self):
        while True:
            logging.info('begin async update.')
            self.anchors = []
            for p in self.scanners:
                yield p.crawl_async()
                self.anchors += p.anchors
            logging.info('async update over.')
            yield tornado.gen.sleep(self.wake_interval)


def register_signal():
    def stop_server(signum, frame):
        logging.info('%s, %s', signum, frame)
        tornado.ioloop.IOLoop.current().stop()

    signal.signal(signal.SIGQUIT, stop_server)
    signal.signal(signal.SIGINT, stop_server)
    signal.signal(signal.SIGTERM, stop_server)


def start_server(port):
    port = int(port)
    sf = ScannerFactory('conf/tv.json')
    settings = {
        'static_path': os.path.join(CUR, 'views/static'),
        'static_url_prefix': 's',
        'template_path': os.path.join(CUR, 'views/dynamic'),
        'xheaders':True,
        'scanner': sf
    }

    app = Application(
        handlers=[
            (r'/jj', JjHandler),
            (r'/', SimpleHandler)
        ],
        **settings
    )

    app.listen(port)
    sf.start_update_job()
    register_signal()
    ioloop = tornado.ioloop.IOLoop.current()
    logging.info('server listen on port: %s', port)
    ioloop.start()


if __name__ == '__main__':
    define('port', default=9999, type=int, help='server port')
    sys.argv.append('--log_to_stderr=true')
    options.parse_command_line()
    start_server(options.port)
