# -*- coding: utf8 -*-
# import json
import requests
from random import randint
from utils import jsonencode as json
from utils.toutiao_reward import TouTiao
from utils.unicomLogin import UnicomClient


class WatchAddFlow(UnicomClient):
    """
        看视频增加流量
    """

    def __init__(self, mobile, password):
        super(WatchAddFlow, self).__init__(mobile, password)
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "accept": "application/json, text/plain, */*",
            "origin": "https://act.10010.com",
            "user-agent": self.useragent,
            "content-type": "application/x-www-form-urlencoded",
            "referer": "https://act.10010.com/SigninApp/mySignin/jumpCollect?yw_code=&desmobile=%s&version=%s" % (
                self.mobile,
                self.version
            ),
            "x-requested-with": "com.sinovatech.unicom.ui"
        })
        self.toutiao = TouTiao(mobile)

    def index(self):
        url = "https://act.10010.com/SigninApp/mySignin/jumpCollect?yw_code=&desmobile=%s&version=%s" % (
            self.mobile,
            self.version
        )
        self.session.get(url=url)

    def queryFlowValue(self):
        url = 'https://act.10010.com/SigninApp/mySignin/queryFlowValue'
        resp = self.session.post(url=url)
        data = resp.json()
        print(json.dumps(data))
        return int(data['watchused'])

    def btnLog(self):
        url = 'https://act.10010.com/SigninApp/mySignin/btnlog'
        data = {
            'stepflag': '22'
        }
        resp = self.session.post(url=url, data=data)
        print(resp.text)

    def addFlow(self, orderId):
        url = 'https://act.10010.com/SigninApp/mySignin/addFlow'
        data = {
            'stepflag': '22',
            'orderId': orderId
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(json.dumps(data))

    def recordLog(self, log):
        record = self.readCookie(f'{self.mobile}WatchAddFlowRecord')
        if not record:
            record = {}
        if len(record) > 30:
            k = list(record.keys())[0]
            record.pop(k)
        record[self.now_date] = log
        self.saveCookie(f'{self.mobile}WatchAddFlowRecord', record)

    def run(self):
        if self.last_login_time.find(self.now_date) == -1:
            self.onLine()
        if self.queryFlowValue() == 3:
            print('今日已完成')
            return
        self.btnLog()
        self.flushTime(randint(15, 25))
        options = {
            'arguments1': '',
            'arguments2': '',
            'codeId': 945535710,
            'remark': '签到任务看视频领流量',
            'channelName': '',
            'ecs_token': self.session.cookies.get('ecs_token')
        }
        orderId = self.toutiao.reward(options)
        self.addFlow(orderId)
        num = self.queryFlowValue()
        self.recordLog(f"[看视频领流量]\n总数:3---完成数:{num}")


if __name__ == '__main__':
    pass
