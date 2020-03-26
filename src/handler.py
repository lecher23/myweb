# coding: utf-8

from __future__ import absolute_import, unicode_literals
import tornado.web


class StockInfo(object):
    def __init__(self, name, code, price, rate):
        self.name = name
        self.code = self.format_code(code)
        self.price = self.format_price(price)
        self.change = self.format_rate(rate)
        
    def format_rate(self, val):
        if val.startswith('-'):
            return '<font class="bg-success">{}%</font>'.format(val)
        return '<font class="bg-danger">{}%</font>'.format(val)

    def format_code(self, val):
        return val.replace("fu_", "")

    def format_price(self, val):
        pos = val.find(".")
        return val[:pos + 3]



class SimpleHandler(tornado.web.RequestHandler):
    def get(self):
        scanner = self.settings['scanner']
        self.render('index.html', anchors=scanner.anchors)

class JjHandler(tornado.web.RequestHandler):
    def get(self):
        data = []
        header = "<table><tr><td>基金</td><td>代码</td><td>当前单价</td><td>涨幅</td><td>更新时间</td></tr>{}</table>"
        uptime = None
        with open("/root/jobs/data/jj.data") as f:
            for line in f:
                item, uptime = self.make_table(line.decode('utf-8'))
                data.append(item)
        #self.write(header.format('\n'.join(data)))
        self.render('main.html', stocks=data, uptime=uptime)

    def make_table(self, line):
        name, code, price, rate, uptime = line.strip().split(',')
        item = StockInfo(name, code, price, rate)
        # return "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(name, code, price, rate, uptime)
        return item, uptime
        
        
