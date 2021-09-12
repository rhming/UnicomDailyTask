# -*- coding: utf8 -*-
import time
import random
import requests


class WoMail(object):

    def __getattribute__(self, name, *args, **kwargs):
        obj = super().__getattribute__(name)
        if type(obj).__name__ == 'method':
            print(obj.__name__.center(64, '#'), self.mobile)
        return obj

    def __init__(self, mobile, openId):
        self.mobile = mobile
        self.openId = openId
        self.session = requests.Session()
        self.session.headers = requests.structures.CaseInsensitiveDict({
            # 'Origin': 'https://nyan.mail.wo.cn',
            'Referer': 'https://nyan.mail.wo.cn/',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; MI 8 SE Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2797 MMWEBSDK/20210501 Mobile Safari/537.36 MMWEBID/107 MicroMessenger/8.0.6.1900(0x28000635) Process/toolsmp WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64',
            'X-Requested-With': 'com.tencent.mm'  # XMLHttpRequest
        })

    @property
    def timestamp(self):
        return int((time.time() + 8 * 60 * 60) * 1000)

    @property
    def randomNum(self):
        return random.random()
