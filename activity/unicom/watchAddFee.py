# -*- coding: utf8 -*-
# import json
import requests
from time import strptime
from random import randint
from utils import jsonencode as json
from utils.toutiao_reward import TouTiao
from utils.unicomLogin import UnicomClient


class WatchAddFee(UnicomClient):

    def __init__(self, mobile, password):
        super(WatchAddFee, self).__init__(mobile, password)
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "accept": "application/json, text/plain, */*",
            "origin": "https://img.client.10010.com",
            "user-agent": self.useragent,
            "content-type": "application/x-www-form-urlencoded",
            "referer": "https://img.client.10010.com/SigininApp/index.html",
            "x-requested-with": "com.sinovatech.unicom.ui"
        })
        self.toutiao = TouTiao(mobile)

    def strptime(self, time_string, format_string='%Y-%m-%d %X'):
        return strptime(time_string, format_string)

    def listTaskInfo(self):
        url = 'https://act.10010.com/SigninApp/multitask/listTaskInfo'
        resp = self.session.post(url=url)
        result = resp.json()
        print(json.dumps(result, indent=4, ensure_ascii=False))
        return result['data']

    def getPrize(self, orderId):
        url = 'https://act.10010.com/SigninApp/prize/getPrize'
        data = {
            'type': 'get',
            'channel': 'taskTelephone',
            'orderId': orderId,
        }
        resp = self.session.post(url=url, data=data)
        print(resp.json())

    def run(self):
        if self.last_login_time.find(self.now_date) == -1:
            self.onLine()
        task = self.listTaskInfo()
        if int(task['achieve']) < int(task['allocation']) and self.strptime(task['curTime']) >= self.strptime(task['expireTime']):
            options = {
                'arguments1': '',
                'arguments2': '',
                'codeId': 946276966,
                'channelName': 'android-签到看视频得话费红包-激励视频',
                'remark': '签到-兑换-看视频做任务得话费',
                'ecs_token': self.session.cookies.get('ecs_token')
            }
            self.flushTime(randint(3, 5))
            orderId = self.toutiao.reward(options)
            self.getPrize(orderId)


if __name__ == '__main__':
    pass
