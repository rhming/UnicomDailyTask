# -*- coding: utf8 -*-
import random
import requests
from utils.common import Common
from urllib.parse import unquote


class WoMail(Common):

    def __init__(self, mobile, openId):
        super(WoMail, self).__init__()
        self.mobile = unquote(mobile)
        self.openId = openId
        self.session = requests.Session()
        self.session.headers = requests.structures.CaseInsensitiveDict({
            # 'Origin': 'https://nyan.mail.wo.cn',
            'Referer': 'https://nyan.mail.wo.cn/',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; MI 8 SE Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2797 MMWEBSDK/20210501 Mobile Safari/537.36 MMWEBID/107 MicroMessenger/8.0.6.1900(0x28000635) Process/toolsmp WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64',
            'X-Requested-With': 'com.tencent.mm'  # XMLHttpRequest
        })

    @property
    def randomNum(self):
        return random.random()

    def recordLog(self, log):
        record = self.readCookie(f'{self.mobile}WoMailRecord')
        if not record:
            record = {}
        if not record.get(self.now_date, False):
            if len(record) > 30:
                k = list(record.keys())[0]
                record.pop(k)
            record[self.now_date] = [log]
        else:
            record[self.now_date].append(log)
        self.saveCookie(f'{self.mobile}WoMailRecord', record)
