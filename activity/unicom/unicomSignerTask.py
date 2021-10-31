# -*- coding: utf8 -*-
# import json
import requests
from random import randint
from utils import jsonencode as json
from utils.msmds import encrypt_mobile
from utils.unicomLogin import UnicomClient


class SignerTask(UnicomClient):

    def __init__(self, mobile, password):
        super(SignerTask, self).__init__(mobile, password)
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "Origin": "https://wxapp.msmds.cn",
            "User-Agent": self.useragent,
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://wxapp.msmds.cn/h5/react_web/unicom/interimPage",
            "X-Requested-With": "com.sinovatech.unicom.ui",
        })

    def login(self):
        url = f'https://wxapp.msmds.cn/jplus/saas/saasUser/login?channelCode=ltelm&channelUserId={self.mobile}'
        resp = self.session.get(url=url, headers={
            'Referer': 'https://wxapp.msmds.cn/h5/react_web/unicom/elemFrontPage?phone='
        })
        data = resp.json()
        print(data)
        self.session.headers.update({
            'Authorization': data['data']['token']
        })

    def findTask(self):
        url = f'https://wxapp.msmds.cn/jplus/h5/unicomTask/findUnicomSignerTask?phone={encrypt_mobile(self.mobile)}'
        data = self.session.post(url=url, headers={
            'Referer': f'https://wxapp.msmds.cn/h5/react_web/unicom/maskIntegralTaskPage?phone={self.mobile}'
        })
        resp = self.session.get(url=url, data=data)
        data = resp.json()
        print(json.dumps(data))
        taskList = data['data']['showTask']
        taskList.extend(data['data']['allTask'])
        return taskList

    def doTask(self, type_, taskId):
        url = 'https://wxapp.msmds.cn/jplus/h5/unicomTask/doTask'
        data = {
            "type": type_,  # "13",
            "taskId": taskId,  # "3a2e9d21cbc14e349ee5b037969b987b",
            "flag": "1",
            "phone": encrypt_mobile(self.mobile),
            "token": self.session.cookies.get('ecs_token'),
        }
        resp = self.session.post(url=url, data=data)
        print(resp.json())

    def drawTaskIntegral(self, type_):
        url = 'https://wxapp.msmds.cn/jplus/h5/unicomTask/drawTaskIntegral'
        data = {
            "phone": encrypt_mobile(self.mobile),
            "token": self.session.cookies.get('ecs_token'),
            "type": type_,
        }
        resp = self.session.post(url=url, data=data)
        print(resp.json())

    def run(self):
        self.login()
        taskList = self.findTask()
        for task in taskList:
            if not task['status']:
                self.doTask(task['type'], task['taskId'] or '3a2e9d21cbc14e349ee5b037969b987b')
                self.flushTime(randint(1, 3))
                self.drawTaskIntegral(task['type'])
                self.flushTime(randint(3, 6))
        for i in [3, 6, 7]:
            self.doTask(i, '3ade00a9030046d28881865e50671178')
            self.flushTime(randint(1, 3))
            self.drawTaskIntegral(i)
            self.flushTime(randint(3, 6))


if __name__ == '__main__':
    pass
