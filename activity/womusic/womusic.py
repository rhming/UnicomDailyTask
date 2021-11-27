# -*- coding: utf8 -*-
import requests
from uuid import uuid4
from utils import jsonencode as json
from random import random, randint
from utils.unicomLogin import UnicomClient
from utils.woapp import encrypt_params, sign


class WoMusic(UnicomClient):

    def __getattribute__(self, name, *args, **kwargs):
        obj = super().__getattribute__(name)
        if type(obj).__name__ == 'method':
            timestamp = self.timestamp
            self.session.headers.update({
                'nonce': str(random()),
                'timestamp': str(timestamp),
                'sign': sign(timestamp),
            })
            # print(obj.__name__.center(64, '#'), self.mobile)
        return obj

    def __init__(self, mobile, password):
        super(WoMusic, self).__init__(mobile, password)
        self.session.headers = requests.structures.CaseInsensitiveDict({
            # "Host": "m.10155.com",
            "Origin": "https://m.10155.com",
            "User-Agent": self.useragent,
            # "content-type": "application/json",
            "content-type": "application/x-www-form-urlencoded",
            "accept": "application/json, text/plain, */*",
            "appid": "3000010831",
            "uid": uuid4().__str__(),
            "Referer": "https://m.10155.com/h5/mactivity/woapphall.html?from=hall&chl=3000010831&yw_code=&desmobile=%s&version=%s" % (
                self.mobile,
                self.version
            ),
            "X-Requested-With": "com.sinovatech.unicom.ui",
        })

    # def refreshHeader(self):
    #     timestamp = self.timestamp
    #     self.session.headers.update({
    #         'nonce': str(random()),
    #         'timestamp': str(timestamp),
    #         'sign': sign(timestamp),
    #     })

    def getLoginCode(self):
        url = 'https://m.10155.com/woapp/h5/login/getCode'
        data = {
            "msisdn": self.mobile
        }
        resp = self.session.post(url=url, json=data, headers={
            "content-type": "application/json"
        })
        data = resp.json()
        return data.get('result', '')

    def videoRingLogin(self, code):
        url = 'https://m.10155.com/woapp/h5/login/videoRingLogin'
        data = {
            "msisdn": self.mobile,
            "code": code
        }
        resp = self.session.post(url=url, json=data, headers={
            "content-type": "application/json"
        })
        data = resp.json()
        self.session.headers.update({
            "accessToken": data['accessToken']
        })
        self.saveCookie(f'{self.mobile}WoMusic', {
            "accessToken": data['accessToken'],
            "t": self.now_date
        })

    def randomList(self):
        url = 'https://m.10155.com/woapp/h5/home/randomList'
        data = {
            "msisdn": self.mobile
        }
        resp = self.session.post(url=url, json=data, headers={
            "content-type": "application/json"
        })
        data = resp.json()
        return data.get('result', {}).get('list', [])

    def integralTaskList(self):
        url = 'https://m.10155.com/woapp/integralTask/integralTaskList'
        resp = self.session.post(url=url)
        data = resp.json()
        print(json.dumps(data, max_depth=4))
        return data

    def getUserIntegralTaskInfo(self, taskType):
        url = 'https://m.10155.com/woapp/integralTask/getUserIntegralTaskInfo'
        data = {'taskType': taskType}
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        # print(json.dumps(data, max_depth=4))
        return data.get('result', {}).get(f'UserIntegralTaskInfo{taskType}', {})

    def doTask(self):
        url = 'https://m.10155.com/woapp/integralTask/doTask'
        data = {
            'taskType': encrypt_params('1'),
            'playDuration': encrypt_params('600'),  # taskDuration
            # 'configKey': encrypt_params('2'),  # taskId
        }
        # data = {
        #     # 'taskType': encrypt_params(''),
        #     # 'taskId': encrypt_params('6cb222e4cb757c6a727173ca1b09d33f'),
        #     # 'taskDuration': encrypt_params('30'),  # taskDuration
        #     # 'configKey': encrypt_params('4'),  # taskId
        #     # 'tab_index': encrypt_params('1'),
        #     # 'url': encrypt_params('/revip'),
        # }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(data)
        # return data

    def likeOper(self, contentId):
        url = 'https://m.10155.com/woapp/my/likeoper'
        data = {
            'objid': contentId,
            'opertype': '1',
            'memberType': '',
        }
        resp = self.session.post(url=url, data=data)
        print(resp.json())

    def run(self):
        self.session.cookies.clear_session_cookies()
        womusic = self.readCookie(f'{self.mobile}WoMusic')
        if not (isinstance(womusic, dict) and womusic.get('t', '') == self.now_date):
            code = self.getLoginCode()
            self.videoRingLogin(code)
            # print('----->')
        else:
            # print(womusic)
            self.session.headers.update({
                "accessToken": womusic['accessToken']
            })
        info = self.getUserIntegralTaskInfo(1)
        if info.get('finishStatus') != 1 and info.get('integral') != info.get('monthTopLimit'):
            self.doTask()
        info = self.getUserIntegralTaskInfo(4)
        if info.get('finishStatus') != 1 and info.get('integral') != info.get('monthTopLimit'):
            for task in self.randomList():
                self.likeOper(task['contentId'])
                self.flushTime(randint(2, 3))


if __name__ == '__main__':
    pass
