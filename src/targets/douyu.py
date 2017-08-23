# coding: utf-8

from __future__ import unicode_literals, absolute_import
from ..datadefine import Anchor, BaseParser


class DouyuParser(BaseParser):
    def __init__(self):
        super(DouyuParser, self).__init__(
            '斗鱼',
            'https://www.douyu.com',
            [
                '/directory/game/How',
                '/directory/game/HOTS'
            ]
        )
        self.low_limit = 2000

    def _extract_anchors(self, doc):
        return doc.find_all('a', 'play-list-link')

    def _extract_anchor(self, anchor):
        title = anchor['title']
        href = self.domain + anchor['href']
        img = anchor.img['data-original']
        owner = anchor.div.p.find("span", "dy-name").text
        hot = self._convert_num(anchor.div.p.find("span", "dy-num").text)
        if hot < self.low_limit:
            return None
        return Anchor(owner=owner, title=title, url=href, img=img, hot=str(hot), comefrom=self.name)
