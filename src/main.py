# coding: utf-8

from __future__ import absolute_import, unicode_literals

import os
import sys
from .handler import SimpleHandler
from tornado.web import Application
from tornado.options import options
import tornado.ioloop

CUR = os.getcwd()


def start_server():
    settings = {
        'static_path': os.path.join(CUR, 'views/static'),
        'static_url_prefix': 's',
        'debug': 'true',
        'template_path': os.path.join(CUR, 'views/dynamic')
    }

    app = Application(
        handlers=[(r'/', SimpleHandler)],
        **settings
    )

    app.listen(9999)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    options.parse_command_line()
    start_server()
