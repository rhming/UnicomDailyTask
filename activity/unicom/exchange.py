# -*- coding: utf8 -*-
import time
import calendar
import requests
from utils.unicomLogin import UnicomClient


class FlowPackage(UnicomClient):

    def __init__(self, mobile, password):
        super(FlowPackage, self).__init__(mobile, password)

        self.session.headers = requests.structures.CaseInsensitiveDict({
            "origin": "https://m.client.10010.com",
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": self.useragent,
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "referer": "https://m.client.10010.com/MyAccount/trafficController/myAccount.htm?yw_code=&desmobile=%s&version=%s" % (
                self.mobile,
                self.version
            )
        })

    def myAccount(self):
        url = 'https://m.client.10010.com/MyAccount/trafficController/myAccount.htm?yw_code=&desmobile=%s&version=%s' % (
            self.mobile,
            self.version
        )
        resp = self.session.get(url=url)
        resp.encoding = 'utf8'
        print(resp.text)

    def exchange(self):
        # ['a_token', 'c_id', 'c_mobile', 'c_sfbm', 'c_version', 'city', 'cw_mutual', 'd_deviceCode', 'ecs_acc', 'ecs_token', 'enc_acc', 'invalid_at', 'jwt', 'login_type', 'random_login', 'route', 't3_token', 'third_token', 'u_account', 'u_areaCode', 'wo_family']
        # self.session.cookies.clear_session_cookies()
        for key in self.session.cookies.get_dict():
            if key in ['ecs_token']:
                continue
            self.session.cookies.pop(key)

        print(self.session.cookies)
        userLogin = ''.join([f'{int(c) + 75}_' for c in self.mobile])
        url = f'https://m.client.10010.com/MyAccount/exchangeWFlow/exchange.htm?userLogin={userLogin}'
        if self.day < 12:
            url = f'https://m.client.10010.com/MyAccount/exchangeDFlow/exchange.htm?userLogin={userLogin}'
        # 月初月末不支持兑换
        # exchangeDFlow 日流量 一天最多一次 一月最多十次
        # exchangeWFlow 多日流量 一天最多4G
        # exchangeFlow 月流量 一天最多一次 一月最多十次
        # exchangeVoice 语音 每次最少50分钟 累计最多200分钟
        # exchangeBillMark 话费 一月最多十次 最多30分钟
        # 2G流量日包 21010621565413402
        # 5G流量日包 21010621461012371
        # 10G流量日包 21010621253114290
        # 4G流量多日包 20080615550312483
        data = {
            "productId": "",
            "productName": "4GB流量多日包",
            "userLogin": userLogin,
            "ebCount": "1",
            "pageFrom": "5"
        }
        if self.day < 12:
            data["productId"] = "21010621565413402"
        elif self.day < 22:
            data["productId"] = "21010621461012371"
        else:
            data["productId"] = "21010621565413402"
        resp = self.session.post(url=url, data=data, allow_redirects=False)
        resp.encoding = 'utf8'
        print(resp.text)

    def run(self):
        year, month, self.day = [
            int(c) for c in self.now_date.split('-')
        ]
        if self.day == 1 or self.day == calendar.monthrange(year, month)[1]:
            print('月初、月末不支持兑换')
            return
        self.flushTime(10)
        self.exchange()
