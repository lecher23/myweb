# coding: utf-8

from __future__ import unicode_literals, absolute_import
from ..datadefine import Anchor, BaseParser


class PandaParser(BaseParser):
    def __init__(self):
        super(PandaParser, self).__init__('熊猫', 'https://www.panda.tv', ['/cate/hearthstone'])
        self.low_limit = 2000

    def _extract_anchors(self, doc):
        return doc.find_all('a', 'video-list-item-wrap')

    def _extract_anchor(self, anchor):
        title = self._extra_text(anchor, '(div, video-info).(span, video-title).text')
        href = self._make_url(self._extra_text(anchor, '[href]'))
        img = self._extra_text(anchor, '(div, video-cover).img.[data-original]')
        owner = self._extra_text(anchor, '(div, video-info).(span, video-nickname).text', 'Unknown')
        hot = self._convert_num(self._extra_text(anchor, '(div, video-info).(span, video-number).text'))
        if hot < self.low_limit:
            return None
        return Anchor(owner=owner, title=title, url=href, img=img, hot=str(hot), comefrom=self.name)
