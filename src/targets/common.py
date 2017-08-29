# coding: utf-8

from __future__ import unicode_literals, absolute_import
from ..scannerbase import Anchor, BaseScanner


class CommonScanner(BaseScanner):
    def __init__(self, conf_name, conf_obj):
        super(CommonScanner, self).__init__(conf_name, conf_obj['domain'], conf_obj['pages'])
        self.items_path = conf_obj['items_path']
        inf_path = conf_obj['info_path']
        self.title_path = inf_path['title']
        self.url_path = inf_path['href']
        self.img_path = inf_path['img']
        self.owner_path = inf_path['owner']
        self.hot_path = inf_path['hot']
        self.low_limit = conf_obj['min_hot']

    def _extract_anchors(self, doc):
        return self._extra_some(doc, self.items_path, [])

    def _extract_anchor(self, anchor):
        title = self._extra_text(anchor, self.title_path, 'Unknown').strip()
        href = self._make_url(self._extra_text(anchor, self.url_path))
        img = self._extra_text(anchor, self.img_path)
        owner = self._extra_text(anchor, self.owner_path, 'Unknown').strip()
        hot = self._convert_num(self._extra_text(anchor, self.hot_path, 'Unknown'))
        if hot < self.low_limit:
            return None
        return Anchor(owner=owner, title=title, url=href, img=img, hot=str(hot), comefrom=self.name)

