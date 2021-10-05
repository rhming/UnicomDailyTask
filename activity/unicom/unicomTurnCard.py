# -*- coding: utf8 -*-
# import json
import requests
from random import randint, choice
from utils import jsonencode as json
from utils.toutiao_reward import TouTiao
from utils.unicomLogin import UnicomClient
from utils.msmds import encrypt_mobile


class TurnCard(UnicomClient):

    def __init__(self, mobile, password):
        super(TurnCard, self).__init__(mobile, password)
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Origin": "https://jxbwlsali.kuaizhan.com",
            "User-Agent": self.useragent,
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://jxbwlsali.kuaizhan.com/0/51/p721841247bc5ac?phone=%s&yw_code=&desmobile=%s&version=%s" % (
                self.mobile,
                self.mobile,
                self.version
            ),
            "X-Requested-With": "com.sinovatech.unicom.ui",
        })
        self.toutiao = TouTiao(mobile)

    def addNum(self, orderId):
        url = 'https://wxapp.msmds.cn/jplus/api/channel/turnCard/addNum'
        data = {
            "channelId": "unicom_turn_card",
            "phone": encrypt_mobile(self.mobile),
            "token": self.session.cookies.get('ecs_token'),
            "videoOrderNo": orderId,
        }
        resp = self.session.post(url=url, data=data)
        print(resp.json())

    def play(self, cardIdx):
        url = 'https://wxapp.msmds.cn/jplus/api/channel/turnCard/play'
        data = {
            "channelId": "unicom_turn_card",
            "phone": encrypt_mobile(self.mobile),
            "token": self.session.cookies.get('ecs_token'),
            "cardIdx": cardIdx,
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(json.dumps(data))

    def getCardsInfo(self):
        url = 'https://wxapp.msmds.cn/jplus/api/channel/turnCard/getCardsInfo'
        resp = self.session.get(url=url)
        data = resp.json()
        # print(json.dumps(data))
        return len(data['data'])

    def getTurnCardInfo(self):
        url = 'https://wxapp.msmds.cn/jplus/api/channel/turnCard/getTurnCardInfo'
        data = {
            "channelId": "unicom_turn_card",
            "phone": encrypt_mobile(self.mobile),
            "token": self.session.cookies.get('ecs_token'),
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(json.dumps(data))
        return data['data']['surplusNum'], [item['index'] for item in data['data']['turnCards']]

    def run(self):
        num = self.getCardsInfo()
        surplusNum, turnCards = self.getTurnCardInfo()
        cards = [i for i in range(1, num + 1) if i not in turnCards]
        if not cards:
            print('机会已用完')
            return
        options = {
            'arguments1': 'AC20200716103629',
            'arguments2': '',
            'codeId': 945535532,
            'channelName': 'new-android-签到领福利赚积分翻牌活动-激励视频',
            'remark': '签到领福利赚积分翻牌活动-激励视频',
            'ecs_token': self.session.cookies.get('ecs_token')
        }
        orderId = self.toutiao.reward(options)
        self.addNum(orderId)
        self.play(choice(cards))
        self.getTurnCardInfo()


if __name__ == '__main__':
    pass
