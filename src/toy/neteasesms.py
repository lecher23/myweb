# coding: utf-8

import time
import random
import hashlib
import requests
import datetime

DEFAULT_CONTENT_TYPE = 'application/x-www-form-urlencoded'


class NeteaseMessage(object):
    def __init__(self, key, secret, tpl_id):
        self._key = key
        self._secret = secret
        self._template_id = tpl_id
        self._host = 'https://api.netease.im/sms/sendtemplate.action'

    def make_header(self):
        nonce = str(random.randint(1, 1000000))
        cur_time = str(int(time.mktime(datetime.datetime.now().timetuple())))
        check_sum = hashlib.sha1('%s%s%s' % (self._secret, nonce, cur_time)).hexdigest()
        headers = {
            'AppKey': self._key,
            'Nonce': nonce,
            'CurTime': cur_time,
            'CheckSum': check_sum,
            'Content-Type': DEFAULT_CONTENT_TYPE,
            'charset': 'utf-8'
        }
        return headers

    def send_msg(self, mobile, contents):
        for content in contents:
            if len(content) > 30:
                raise ValueError('content too long:{}'.format(content))
        body = 'templateid={}&mobiles=["{}"]&params=[{}]'.format(
            self._template_id, mobile, ','.join(("\"{}\"".format(item) for item in contents)))
        r = requests.post(self._host, headers=self.make_header(), data=body)
        print r.content
