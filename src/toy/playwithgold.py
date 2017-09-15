# coding:utf-8

from __future__ import unicode_literals
import json
import heapq
import datetime
import requests
from collections import namedtuple

GoldPrice = namedtuple('GoldPrice', 'now high low close up_time')

headers = {
    "Origin": "http://gold.cnfol.com",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36",
    "Referer": "http://gold.cnfol.com/fol_inc/v6.0/Gold/Gold99.shtml",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8"
}


class GoldCrawl(object):
    def __init__(self):
        self.session = requests.session()
        self._sell_point = 280.0
        self._buy_point = 271.0
        self._tag = '黄金99.99'
        self._today_api = "http://gold.cnfol.com/fol_inc/v6.0/Gold/goldhq/json_table/td_tableinfo.json"
        self._his_api = "http://gold.cnfol.com/fol_inc/v6.0/Gold/goldhq/json/g/au9999/KlDay.json?t=0.5818640350903175"
        self._decide_factor = 3

    def analyze_history_price(self):
        r = self.session.post(self._his_api, headers=headers)
        obj = json.loads(r.content)
        n_price = []
        for row in obj:
            # 时间，开盘，最高，最低，收盘
            row[0] = datetime.datetime.fromtimestamp(row[0] / 1000.0).strftime('%Y-%m-%d')
            n_price.append(row[1])
        n = len(n_price) // 3
        low_n = heapq.nsmallest(n, n_price)
        self._buy_point = sum(low_n) / len(low_n)
        high_n = heapq.nlargest(n, n_price)
        self._sell_point = sum(high_n) / len(high_n)
        print "高点: %.2f， 低点: %.2f" % (self._sell_point, self._buy_point)

    def analyze_today_price(self):
        r = self.session.post(self._today_api, headers=headers)
        obj = json.loads(r.content)
        found = None
        for item in obj['data']:
            if item['name'] == self._tag:
                found = item
                break
        if not found:
            print "no item."
            return False
        ts = datetime.datetime.fromtimestamp(int(found['QuoteTime']))
        price_item = GoldPrice(
            now=float(found['Last']), high=float(found['High']),
            low=float(found['Low']), close=float(found['LastClose']), up_time=ts
        )
        print '最新价格: %s, 最高价: %s, 最低价: %s\n' \
              '昨日收盘价: %s\n' \
              '更新时间: %s' % (found['Last'], found['High'], found['Low'], found['LastClose'], ts)
        if price_item.now > self._sell_point:
            print '高于历史平均值:%.2f, 建议卖出' % self._sell_point
        elif price_item.now < self._buy_point:
            print '低于历史平均值:%.2f, 建议买入' % self._buy_point
        return True


def main():
    gc = GoldCrawl()
    gc.analyze_history_price()
    gc.analyze_today_price()


if __name__ == '__main__':
    main()
