# -*- coding: utf8 -*-
# import json
import requests
from random import randint, choice
from utils import jsonencode as json
from utils.toutiao_reward import TouTiao
from utils.unicomLogin import UnicomClient
from utils.msmds import encrypt_mobile


class ScratchCard(UnicomClient):
    """
        活动过期
    """

    def __init__(self, mobile, password):
        super(ScratchCard, self).__init__(mobile, password)
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "Origin": "https://wxapp.msmds.cn",
            "User-Agent": self.useragent,
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://wxapp.msmds.cn/h5/react_web/unicom/luckCardPage?source=unicom&yw_code=&desmobile=%s&version=%s" % (
                self.mobile,
                self.version
            ),
            "X-Requested-With": "com.sinovatech.unicom.ui",
        })
        self.toutiao = TouTiao(mobile)

    def index(self):
        url = "https://wxapp.msmds.cn/h5/react_web/unicom/luckCardPage?source=unicom&yw_code=&desmobile=%s&version=%s" % (
            self.mobile,
            self.version
        )
        _ = self.session.get(url=url)

    def getScratchCardNum(self):
        url = 'https://wxapp.msmds.cn/jplus/api/scratchCardRecord/getScratchCardNum'
        data = {
            "channelId": "unicom_scratch_card",
            "phone": encrypt_mobile(self.mobile),
            "token": self.session.cookies.get('ecs_token'),
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(json.dumps(data))
        return data['data']['surplusNum'], data['data']['playNum']

    def addScratchCardNum(self, orderId):
        url = 'https://wxapp.msmds.cn/jplus/api/scratchCardRecord/addScratchCardNum'
        data = {
            "channelId": "unicom_scratch_card",
            "phone": encrypt_mobile(self.mobile),
            "token": self.session.cookies.get('ecs_token'),
            "videoOrderNo": orderId,
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(json.dumps(data))

    def scratchCard(self):
        url = 'https://wxapp.msmds.cn/jplus/api/scratchCardRecord/scratchCard'
        data = {
            "channelId": "unicom_scratch_card",
            "phone": encrypt_mobile(self.mobile),
            "token": self.session.cookies.get('ecs_token'),
            "flag": "",
            "taskId": "",
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(json.dumps(data))
        return data['data']['id'], data['data']['canDouble']

    def newStoreySignToUnicom(self):
        url = 'https://wxapp.msmds.cn/jplus/h5/unicomSignTask/newStoreySignToUnicom'
        data = {
            "phone": self.mobile,
            "taskId": "cfb63b63e7a64ea7bf21b8113d28ae1a",
        }
        resp = self.session.post(url=url, data=data)
        print(resp.json())

    # def integralTask(self):
    #     options = {
    #         'arguments1': 'AC20200716103629',
    #         'arguments2': 'a42de1cf969945eb87b529c4763ab6e5',
    #         'codeId': 945535637,
    #         'channelName': 'new-android-签到小游戏霸王餐积分翻倍-激励视频',
    #         'remark': '签到小游戏翻倍得积分',
    #         'ecs_token': self.session.cookies.get('ecs_token')
    #     }
    #     account = {
    #         "accountChannel": "517050707",
    #         "accountUserName": "5170507071",
    #         "accountPassword": "123456",
    #         "accountToken": "638d17ae37a648e9a786bb973d1c4c7b",
    #     }
    #     if self.taskcallbackquery(options['arguments1'], options['arguments2']):
    #         orderId = self.toutiao.reward(options)
    #         self.taskcallbackdotasks(options['arguments1'], options['arguments2'], orderId, options['remark'])

    def run(self):
        surplusNum, playNum = self.getScratchCardNum()
        if playNum == 5:
            print('机会已用完')
            return
        if not surplusNum:
            options = {
                'arguments1': '',
                'arguments2': '',
                'codeId': 945535641,
                'channelName': 'new-android-签到小游戏霸王餐得抽奖次数-激励视频',
                'remark': '签到页小游戏',
                'ecs_token': self.session.cookies.get('ecs_token')
            }
            orderId = self.toutiao.reward(options)
            self.addScratchCardNum(orderId)
        self.scratchCard()
        self.newStoreySignToUnicom()


if __name__ == '__main__':
    pass
