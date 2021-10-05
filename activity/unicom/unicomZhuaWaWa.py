# -*- coding: utf8 -*-
# import json
import requests
from random import randint, choice
from utils import jsonencode as json
from utils.toutiao_reward import TouTiao
from utils.unicomLogin import UnicomClient
from utils.msmds import encrypt_mobile


class ZhuaWaWa(UnicomClient):

    def __init__(self, mobile, password):
        super(ZhuaWaWa, self).__init__(mobile, password)
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "Origin": "https://wxapp.msmds.cn",
            "User-Agent": self.useragent,
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://wxapp.msmds.cn/h5/react_web/unicom/grabdollPage?source=unicom&yw_code=&desmobile=%s&version=%s" % (
                self.mobile,
                self.version
            ),
            "X-Requested-With": "com.sinovatech.unicom.ui",
        })
        self.toutiao = TouTiao(mobile)

    def index(self):
        url = 'https://wxapp.msmds.cn/jplus/api/channelGrabDoll/index'
        data = {
            "channelId": "LT_channel",
            "phone": encrypt_mobile(self.mobile),
            "token": self.session.cookies.get('ecs_token'),
            "sourceCode": "lt_zhuawawa",
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(json.dumps(data))
        return data['data']['leftTime'], data['data']['grabDollAgain']

    def getPlayTimes(self):
        url = 'https://wxapp.msmds.cn/jplus/api/channelGrabDoll/getPlayTimes'
        data = {
            "channelId": "LT_channel",
            "phone": encrypt_mobile(self.mobile),
            "token": self.session.cookies.get('ecs_token'),
            "sourceCode": "lt_zhuawawa",
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(json.dumps(data))
        return data['data']['playTimes']

    def startGame(self):
        url = 'https://wxapp.msmds.cn/jplus/api/channelGrabDoll/startGame'
        data = {
            "channelId": "LT_channel",
            "phone": encrypt_mobile(self.mobile),
            "token": self.session.cookies.get('ecs_token'),
            "sourceCode": "lt_zhuawawa",
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(json.dumps(data))
        return data['data']

    def playGrabDoll(self, item: dict):
        url = 'https://wxapp.msmds.cn/jplus/api/channelGrabDoll/playGrabDoll'
        data = {
            "channelId": "LT_channel",
            "phone": encrypt_mobile(self.mobile),
            "token": self.session.cookies.get('ecs_token'),
            "sourceCode": "lt_zhuawawa",
            "goodsImg": item['goodsImg'],
            "goodsName": item['goodsName'],
            "machineGoodsId": item['machineGoodsId'],
            "prizeNum": item['prizeNum'],
            "prizeType": item['prizeType'],
        }
        '''
            "grabDetailedId": null,
            "machineGoodsId": 28,
            "goodsName": "买什么都省会员（月卡）",
            "goodsImg": "https://alicdn.msmds.cn/liantong/zwwhuiyuan3x.png",
            "prizeType": 2,
            "prizeNum": 1,
            "doubleNum": 0,
            "double": false,
            "grabDollAgain": false
        '''
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(json.dumps(data))
        item.update(data['data'])
        return item

    def sign(self):
        url = 'https://wxapp.msmds.cn/jplus/h5/unicomSignTask/sign'
        data = {
            "phone": self.mobile,
            "taskId": "4394389e42ce44bb85afcad1cdc9a514",
        }
        resp = self.session.post(url=url, data=data)
        print(resp.json())

    def playAgainByLookingVideos(self, orderId):
        url = 'https://wxapp.msmds.cn/jplus/api/channelGrabDoll/playAgainByLookingVideos'
        data = {
            "channelId": "LT_channel",
            "phone": encrypt_mobile(self.mobile),
            "token": self.session.cookies.get('ecs_token'),
            "sourceCode": "lt_zhuawawa",
            "videoOrderNo": orderId,
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(json.dumps(data))

    # def creditsDoubleByLookingVideos(self, item: dict):
    #     url = 'https://wxapp.msmds.cn/jplus/api/channelGrabDoll/creditsDoubleByLookingVideos'
    #     data = {
    #         "channelId": "LT_channel",
    #         "phone": encrypt_mobile(self.mobile),
    #         "token": self.session.cookies.get('ecs_token'),
    #         "sourceCode": "lt_zhuawawa",
    #         "grabDetailedId": item['grabDetailedId'],
    #         "prizeNum": item['prizeNum'],
    #     }
    #     resp = self.session.post(url=url, data=data)
    #     print(resp.json())

    def getGeneralBox(self):
        url = 'https://wxapp.msmds.cn/jplus/api/channelGrabDoll/getGeneralBox'
        data = {
            "channelId": "LT_channel",
            "phone": encrypt_mobile(self.mobile),
            "token": self.session.cookies.get('ecs_token'),
            "sourceCode": "lt_zhuawawa",
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(data)
        return data['code']

    def openGeneralBox(self, orderId=''):
        url = 'https://wxapp.msmds.cn/jplus/api/channelGrabDoll/openGeneralBox'
        data = {
            "channelId": "LT_channel",
            "phone": encrypt_mobile(self.mobile),
            "token": self.session.cookies.get('ecs_token'),
            "sourceCode": "lt_zhuawawa",
            "isNew": "false",
            # "orderId": orderId,
        }
        resp = self.session.post(url=url, data=data)
        print(resp.json())

    def run(self):
        leftTime, grabDollAgain = self.index()
        if not grabDollAgain:
            print('机会已用完')
            return
        if not leftTime:
            options = {
                'arguments1': '',
                'arguments2': '',
                'codeId': 945719787,
                'channelName': 'android-签到小游戏开心抓大奖-激励视频',
                'remark': '签到页小游戏',
                'ecs_token': self.session.cookies.get('ecs_token')
            }
            orderId = self.toutiao.reward(options)
            self.playAgainByLookingVideos(orderId)
        item = self.startGame()
        if item:
            item = self.playGrabDoll(item)
            # if item.get('double', ''):
            #     self.creditsDoubleByLookingVideos(item)
        self.sign()
        if self.getPlayTimes() == 3:
            self.getGeneralBox()
            self.openGeneralBox()


if __name__ == '__main__':
    pass
