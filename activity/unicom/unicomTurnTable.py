# -*- coding: utf8 -*-
# import json
import requests
from random import randint, choice
from utils import jsonencode as json
from utils.toutiao_reward import TouTiao
from utils.unicomLogin import UnicomClient
from utils.msmds import encrypt_mobile


class TurnTable(UnicomClient):

    def __init__(self, mobile, password):
        super(TurnTable, self).__init__(mobile, password)
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "Origin": "https://wxapp.msmds.cn",
            "User-Agent": self.useragent,
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://wxapp.msmds.cn/h5/react_web/unicom/turntablePage?source=unicom&yw_code=&desmobile=%s&version=%s" % (
                self.mobile,
                self.version
            ),
            "X-Requested-With": "com.sinovatech.unicom.ui",
        })
        self.toutiao = TouTiao(mobile)

    def list(self):
        url = 'https://wxapp.msmds.cn/jplus/api/change/luck/draw/gift/v1/list'
        data = {
            "channelId": "LT_channel",
            "phone": encrypt_mobile(self.mobile),
            "token": self.session.cookies.get('ecs_token'),
            # "sourceCode": "lt_turntable",
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(json.dumps(data))
        return data['data']['playCounts'], data['data']['useCount']

    def getPlayTimes(self):
        url = 'https://wxapp.msmds.cn/jplus/api/change/luck/draw/gift/v1/getPlayTimes'
        data = {
            "channelId": "LT_channel",
            "phone": encrypt_mobile(self.mobile),
            "token": self.session.cookies.get('ecs_token'),
            "sourceCode": "lt_turntable",
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(json.dumps(data))
        return data['data']['playTimes']

    def playLuckDraw(self):
        url = 'https://wxapp.msmds.cn/jplus/api/change/luck/draw/gift/v1/playLuckDraw'
        data = {
            "phone": encrypt_mobile(self.mobile),
            "token": self.session.cookies.get('ecs_token'),
            "channelId": "LT_channel",
            "code": "",
            "flag": "",
            "taskId": "",
            "sourceCode": "lt_turntable",
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(data)
        return data

    def sign(self):
        url = 'https://wxapp.msmds.cn/jplus/h5/unicomSignTask/sign'
        data = {
            "phone": self.mobile,
            "taskId": "0f2e1cc1f550433abc86e0ef1b380839",
        }
        resp = self.session.post(url=url, data=data)
        print(resp.json())

    def video(self, orderId):
        url = 'https://wxapp.msmds.cn/jplus/api/change/luck/draw/gift/v1/liantong/look/video'
        data = {
            "channelId": "LT_channel",
            "phone": encrypt_mobile(self.mobile),
            "token": self.session.cookies.get('ecs_token'),
            "sourceCode": "lt_turntable",
            "videoOrderNo": orderId,
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(json.dumps(data))

    def getGeneralBox(self):
        url = 'https://wxapp.msmds.cn/jplus/api/change/luck/draw/gift/v1/getGeneralBox'
        data = {
            "channelId": "LT_channel",
            "phone": encrypt_mobile(self.mobile),
            "token": self.session.cookies.get('ecs_token'),
            "sourceCode": "lt_turntable",
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(data)
        return data['code']

    def openGeneralBox(self, orderId):
        url = 'https://wxapp.msmds.cn/jplus/api/change/luck/draw/gift/v1/openGeneralBox'
        data = {
            "channelId": "LT_channel",
            "phone": encrypt_mobile(self.mobile),
            "token": self.session.cookies.get('ecs_token'),
            "sourceCode": "lt_turntable",
            "isNew": "false",
            "orderId": orderId,
        }
        resp = self.session.post(url=url, data=data)
        print(resp.json())

    def run(self):
        playCounts, useCount = self.list()
        if useCount == 5:
            print('机会已用完')
            return
        if not playCounts:
            options = {
                'arguments1': '',
                'arguments2': '',
                'codeId': 946169925,
                'channelName': 'android-签到小游戏幸运转盘-激励视频',
                'remark': '签到页小游戏',
                'ecs_token': self.session.cookies.get('ecs_token')
            }
            # self.flushTime(randint(5, 10))
            orderId = self.toutiao.reward(options)
            self.video(orderId)
        self.playLuckDraw()
        self.sign()
        if self.getPlayTimes() == 3:
            if self.getGeneralBox() == 200 or True:
                options = {
                    'arguments1': '',
                    'arguments2': '',
                    'codeId': 946169925,
                    'channelName': 'android-签到小游戏幸运转盘-激励视频',
                    'remark': '签到页小游戏',
                    'ecs_token': self.session.cookies.get('ecs_token')
                }
                orderId = self.toutiao.reward(options)
                self.openGeneralBox(orderId)


if __name__ == '__main__':
    pass
