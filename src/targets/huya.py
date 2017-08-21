# coding: utf-8

from __future__ import unicode_literals, absolute_import
import logging
import requests
from bs4 import BeautifulSoup
from ..datadefine import Anchor, BaseParser


class HuyaParser(BaseParser):
    def __init__(self):
        super(HuyaParser, self).__init__(
            '虎牙',
            'https://www.huya.com',
            [
                '/g/hearthstone'
            ]
        )
        self.low_limit = 2000

    def _crawl(self, page):
        r = requests.get(page, verify=False)
        doc = BeautifulSoup(r.content, 'html5lib')
        anchors = doc.find_all('li', 'game-live-item')
        for anchor in anchors:
            try:
                title = anchor.find('a', 'title')['title']
                href = anchor.a['href']
                img = anchor.a.span.img['data-original']
                owner = anchor.find('i', 'nick')['title']
                hot = self._convert_num(anchor.find("i", "js-num").text)
                if hot < self.low_limit:
                    continue
            except:
                logging.exception('process huya anchor info %s failed.', anchor)
            else:
                self.anchors.append(
                    Anchor(owner=owner, title=title, url=href, img=img, hot=str(hot), comefrom=self.name))
