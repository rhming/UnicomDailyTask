# -*- coding: utf8 -*-
# import json
import requests
from random import randint, choice
from utils import jsonencode as json
from utils.toutiao_reward import TouTiao
from utils.unicomLogin import UnicomClient
from utils.msmds import encrypt_mobile

class Dxlottery(UnicomClient):
    def __init__(self, mobile, password):
        super(Dxlottery, self).__init__(mobile, password)
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Origin": "https://img.client.10010.com",
            "User-Agent": self.useragent,
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://img.client.10010.com/",
            "X-Requested-With": "com.sinovatech.unicom.ui",
        })
        self.toutiao = TouTiao(mobile)

    def winterTwoStatus(self):
        status = True
        url = 'https://m.client.10010.com/welfare-mall-front/mobile/winterTwo/winterTwoShop/v1'
        resp = self.session.post(url=url)
        data = resp.json()
        print(json.dumps(data))
        if data['resdata']['code'] != '0000':
            print('获取东奥积分活动状态失败', data['resdata']['desc'])
        else:
            status = True
            print('获取东奥积分活动状态成功 已连续领取%s天' %(data['resdata']['signDays']))
        return status

    def winterTwoGetIntegral(self):
        url = 'https://m.client.10010.com/welfare-mall-front/mobile/winterTwo/getIntegral/v1'
        resp = self.session.post(url=url)
        data = resp.json()
        print(json.dumps(data))
        if data['resdata']['code'] != '0000':
            print('冬奥积分活动领取失败', data['resdata']['desc'])
        else:
            self.recordLog('冬奥积分活动领取成功')
            print('冬奥积分活动领取成功')

    def dxIntegralEveryDay(self):
        url = 'https://m.client.10010.com/welfare-mall-front/mobile/integral/gettheintegral/v1'
        resp = self.session.post(url=url)
        data = resp.json()
        print(json.dumps(data))
        if data['code'] != '0':
            print('获取东奥积分活动状态失败', data['msg'])
        else:
            self.recordLog('每日定向积分领取成功')
            print('每日定向积分领取成功')

    def run(self):
        if not self.winterTwoStatus():
            self.winterTwoGetIntegral()
            self.winterTwoStatus()
            self.flushTime(5)
            self.dxIntegralEveryDay()

if __name__ == '__main__':
    pass
