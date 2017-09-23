# coding:utf-8

from __future__ import unicode_literals
import json
import heapq
import datetime
import requests
import argparse
from collections import namedtuple
from neteasesms import NeteaseMessage

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
        self.price_info = None
        self.sell_point = 280.0
        self.buy_point = 271.0

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
        self.buy_point = sum(low_n) / len(low_n)
        high_n = heapq.nlargest(n, n_price)
        self.sell_point = sum(high_n) / len(high_n)

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
        self.price_info = GoldPrice(
            now=float(found['Last']), high=float(found['High']),
            low=float(found['Low']), close=float(found['LastClose']), up_time=ts
        )

    def __repr__(self):
        strs = list()
        strs.append("高点: %.2f， 低点: %.2f" % (self.sell_point, self.buy_point))
        strs.append('最新价格: %s, 最高价: %s, 最低价: %s\n昨日收盘价: %s\n更新时间: %s' % (
            self.price_info.now, self.price_info.high, self.price_info.low,
            self.price_info.close, self.price_info.up_time))
        if self.price_info.now > self.sell_point:
            strs.append('高于历史平均值:%.2f, 建议卖出' % self.sell_point)
        elif self.price_info.now < self.buy_point:
            strs.append('低于历史平均值:%.2f, 建议买入' % self.buy_point)
        return '\n'.join(strs).encode('utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', type=str, dest='key', help='yunxin key')
    parser.add_argument('-s', type=str, dest='secret', help='yunxin secret')
    parser.add_argument('-t', type=str, dest='template_id', help='yunxin message template id')
    parser.add_argument('-p', type=int, dest='phone', help='phone number to sent')
    args = parser.parse_args()

    nm = NeteaseMessage(args.key, args.secret, args.template_id)
    # nm.send_msg(args.phone, [])

    gc = GoldCrawl()
    gc.analyze_history_price()
    gc.analyze_today_price()
    print(gc)


if __name__ == '__main__':
    main()
