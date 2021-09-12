# -*- coding: utf8 -*-
import time
# import json
import requests
from random import randint
from utils.unicomLogin import UnicomClient
from utils.toutiao_reward import TouTiao
from utils import jsonencode as json


class SigninApp(UnicomClient):
    """
        联通日常签到
    """

    def __init__(self, mobile, password):
        super(SigninApp, self).__init__(mobile, password)
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "accept": "application/json, text/plain, */*",
            "origin": "https://img.client.10010.com",
            "user-agent": self.useragent,
            "content-type": "application/x-www-form-urlencoded",
            "referer": "https://img.client.10010.com/SigininApp/index.html",
            "x-requested-with": "com.sinovatech.unicom.ui"
        })
        self.hasDouble = False
        self.toutiao = TouTiao(mobile)

    def listTaskInfo(self):
        url = 'https://act.10010.com/SigninApp/convert/listTaskInfo'
        resp = self.session.post(url=url)
        result = resp.json()
        print(json.dumps(result, indent=4, ensure_ascii=False))
        return result['data']['paramsList']

    def doTask(self, item, orderId):
        url = 'https://act.10010.com/SigninApp/task/doTask'
        data = {
            "markId": item['markId'],
            "orderId": orderId,
            "prizeType": item['prizeType'],
        }
        resp = self.session.post(url=url, data=data)
        print(resp.json())

    def getIntegral(self):
        url = 'https://act.10010.com/SigninApp/signin/getIntegral'
        resp = self.session.post(url=url)
        print(resp.json())

    def getContinuous(self):
        url = 'https://act.10010.com/SigninApp/signin/getContinuous'
        resp = self.session.post(url=url)
        result = resp.json()
        print(json.dumps(result, indent=4, ensure_ascii=False))
        data = result['data']  # ['daySignList']
        doubleBtn = data['doubleBtn']
        if int(doubleBtn['click']) == 1:
            self.hasDouble = True
        if int(data['todaySigned']) == 0:
            print("今日已签到")
            return True

    def getGoldTotal(self):
        url = 'https://act.10010.com/SigninApp/signin/getGoldTotal'
        resp = self.session.post(url=url)
        print(resp.json())

    def signIn(self):
        url = 'https://act.10010.com/SigninApp/signin/daySign'
        resp = self.session.post(url=url)
        resp.encoding = 'utf8'
        data = resp.json()
        print(json.dumps(data, indent=4, ensure_ascii=False))

    def bannerAdPlayingLogo(self, orderId):
        # signin
        url = 'https://act.10010.com/SigninApp/task/bannerAdPlayingLogo'
        data = {
            "orderId": orderId
        }
        resp = self.session.post(url=url, data=data)
        print(json.dumps(resp.json(), indent=4, ensure_ascii=False))

    def run(self):
        now_date = time.strftime(
            "%Y-%m-%d",
            time.localtime(self.timestamp / 1000)
        )
        if self.last_login_time.find(now_date) == -1:
            self.onLine()
        if not self.getContinuous():
            self.signIn()
            # self.getGoldTotal()
            # self.getIntegral()
            self.getContinuous()
        if self.hasDouble:
            time.sleep(randint(10, 15))
            options = {
                'arguments1': '',
                'arguments2': '',
                'codeId': 945535743,
                'remark': '签到看视频翻倍得积分',
                'channelName': '签到成功看视频再得奖',
                'ecs_token': self.session.cookies.get('ecs_token')
            }
            orderId = self.toutiao.reward(options)
            self.bannerAdPlayingLogo(orderId)
        for item in self.listTaskInfo():
            if int(item['accomplish']) or not int(item['click']):
                continue
            self.flushTime(randint(25, 30))
            options = {
                'arguments1': '',
                'arguments2': '',
                'codeId': 945558051,
                'remark': '签到气泡任务',
                'channelName': '签到页头气泡看视频得奖励',
                'ecs_token': self.session.cookies.get('ecs_token')
            }
            orderId = self.toutiao.reward(options)
            self.doTask(item, orderId)


if __name__ == '__main__':
    pass
