# -*- coding: utf8 -*-
import requests
from requests.structures import CaseInsensitiveDict
from activity.woread.woread import WoRead
from utils.ngworead import cryptojs_encrypt, encrypt, auth_sign
from random import randint


class NGWoRead(WoRead):

    def __init__(self, mobile, _=None):
        super(NGWoRead, self).__init__(mobile, _)
        self.mobile = mobile
        self.version = "android@9.0001"
        self.session = requests.Session()
        self.session.headers = CaseInsensitiveDict({
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://10010.woread.com.cn",
            "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; MI 8 SE Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36; unicom{version:%s,desmobile:%s};devicetype{deviceBrand:Xiaomi,deviceModel:MI 8 SE};{yw_code:}" % (
                self.version,
                self.mobile
            ),
            "Content-Type": "application/json;charset=UTF-8",
            "Referer": "https://10010.woread.com.cn/ng_woread/",
            "X-Requested-With": "com.sinovatech.unicom.ui",
        })
        self.appId = '10000002'
        self.config = {}
        self.session.cookies.clear_session_cookies()

    @property
    def formatTime(self):
        return (self.now_date + self.now_time).replace('-', '').replace(':', '')

    def getAccessToken(self):
        timestamp = self.timestamp
        sign = auth_sign(self.appId, timestamp)
        url = f'https://10010.woread.com.cn/ng_woread_service/rest/app/auth/{self.appId}/{timestamp}/{sign}'
        data = {
            'sign': cryptojs_encrypt({
                'timestamp': self.formatTime
            })
        }
        resp = self.session.post(url=url, json=data)
        resp.encoding = 'utf8'
        data = resp.json()
        print(data)
        # {
        #     'code': '0000', 'innercode': None, 'message': 'success',
        #     'data': {'accesstoken': 'ODZERTZCMjA1NTg1MTFFNDNFMThDRDYw'},
        #     'success': True
        # }
        self.accesstoken = data.get('data', {}).get('accesstoken', 'ODZERTZCMjA1NTg1MTFFNDNFMThDRDYw')
        self.config.update({
            'accesstoken': self.accesstoken
        })
        self.session.headers.update({
            'accesstoken': self.accesstoken
        })

    def login(self):
        url = 'https://10010.woread.com.cn/ng_woread_service/rest/account/login'
        data = {
            'sign': encrypt(
                {'phone': self.mobile, 'timestamp': self.formatTime},
                self.accesstoken
            )
        }
        resp = self.session.post(url=url, json=data)
        resp.encoding = 'utf8'
        data = resp.json()
        data = data['data']
        self.config.update(data)
        self.config.update({
            't': self.now_date
        })
        print(data)
        # {
        #     'userindex': , 'verifycode': '', 'isshoutingnew': 0,
        #     'userid': '', 'token': '',
        #     'phone': '', 'isFreeUser': 0
        # }
        self.saveCookie(f'{self.mobile}NGWoRead', self.config)
        return data.get('data', {})

    def queryActiveInfo(self, retry=1):
        url = 'https://10010.woread.com.cn/ng_woread_service/rest/activity/yearEnd/queryActiveInfo'
        data = {
            'sign': encrypt(
                {
                    'timestamp': self.formatTime,
                    'token': self.config['token'],
                    'userId': self.config['userid'],
                    'userIndex': self.config['userindex'],
                    'userAccount': self.mobile,
                    'verifyCode': self.config['verifycode']
                },
                self.config['accesstoken']
            )
        }
        resp = self.session.post(url=url, json=data)
        data = resp.json()
        if data.get('message', '') == '用户登录已过期' and retry > 0:
            self.getAccessToken()
            self.login()
            return self.queryActiveInfo(retry - 1)
        data = data.get('data', {})
        data.update({'activerule': ''})
        print(data)
        return data.get('activeindex', '181')

    def queryUserScore(self):
        url = 'https://10010.woread.com.cn/ng_woread_service/rest/activity/yearEnd/queryUserScore'
        data = {
            'sign': encrypt(
                {
                    'activeIndex': self.config['activeindex'],
                    'timestamp': self.formatTime,
                    'token': self.config['token'],
                    'userId': self.config['userid'],
                    'userIndex': self.config['userindex'],
                    'userAccount': self.mobile,
                    'verifyCode': self.config['verifycode']
                },
                self.config['accesstoken']
            )
        }
        resp = self.session.post(url=url, json=data)
        data = resp.json()
        data = data['data']
        print(data)
        return data.get('validScore', 0)

    def queryScoreWay(self):
        url = 'https://10010.woread.com.cn/ng_woread_service/rest/activity/yearEnd/queryScoreWay'
        data = {
            'sign': encrypt(
                {
                    'activeIndex': self.config['activeindex'],
                    'timestamp': self.formatTime,
                    'token': self.config['token'],
                    'userId': self.config['userid'],
                    'userIndex': self.config['userindex'],
                    'userAccount': self.mobile,
                    'verifyCode': self.config['verifycode']
                },
                self.config['accesstoken']
            )
        }
        resp = self.session.post(url=url, json=data)
        data = resp.json()
        data = data.get('data', [])
        return data

    def queryAdList(self):
        url = 'https://10010.woread.com.cn/ng_woread_service/rest/activity/yearEnd/queryAdList'
        data = {
            'sign': encrypt(
                {
                    'activeIndex': self.config['activeindex'],
                    'timestamp': self.formatTime,
                    'token': self.config['token'],
                    'userId': self.config['userid'],
                    'userIndex': self.config['userindex'],
                    'userAccount': self.mobile,
                    'verifyCode': self.config['verifycode']
                },
                self.config['accesstoken']
            )
        }
        resp = self.session.post(url=url, json=data)
        data = resp.json()
        data = data.get('data', {})
        print(data)
        return data.get('daylimit', 5), (data.get('gainnum', 0) or 0), data.get('mapList', [])

    def obtainScoreByAd(self, value='947728124'):
        url = 'https://10010.woread.com.cn/ng_woread_service/rest/activity/yearEnd/obtainScoreByAd'
        data = {
            'sign': encrypt(
                {
                    'value': value,
                    'timestamp': self.formatTime,
                    'token': self.config['token'],
                    'userId': self.config['userid'],
                    'userIndex': self.config['userindex'],
                    'userAccount': self.mobile,
                    'verifyCode': self.config['verifycode']
                },
                self.config['accesstoken']
            )
        }
        resp = self.session.post(url=url, json=data)
        data = resp.json()
        print(data)

    def checkUserTakeActive(self, activeIndex):
        url = 'https://10010.woread.com.cn/ng_woread_service/rest/activity/checkUserTakeActive'
        data = {
            'sign': encrypt(
                {
                    'activeIndex': activeIndex,
                    'timestamp': self.formatTime,
                    'token': self.config['token'],
                    'userId': self.config['userid'],
                    'userIndex': self.config['userindex'],
                    'userAccount': self.mobile,
                    'verifyCode': self.config['verifycode']
                },
                self.config['accesstoken']
            )
        }
        resp = self.session.post(url=url, json=data)
        data = resp.json()
        print(data)
        return data.get('data', 0)

    def userTakeActive(self, activeIndex):
        url = 'https://10010.woread.com.cn/ng_woread_service/rest/activity/userTakeActive'
        data = {
            'sign': encrypt(
                {
                    'activeIndex': activeIndex,
                    'timestamp': self.formatTime,
                    'token': self.config['token'],
                    'userId': self.config['userid'],
                    'userIndex': self.config['userindex'],
                    'userAccount': self.mobile,
                    'verifyCode': self.config['verifycode']
                },
                self.config['accesstoken']
            )
        }
        resp = self.session.post(url=url, json=data)
        data = resp.json()
        print(data)
        return data

    def handleDrawLottery(self):
        url = 'https://10010.woread.com.cn/ng_woread_service/rest/activity/yearEnd/handleDrawLottery'
        data = {
            'sign': encrypt(
                {
                    'activeIndex': self.config['activeindex'],
                    'timestamp': self.formatTime,
                    'token': self.config['token'],
                    'userId': self.config['userid'],
                    'userIndex': self.config['userindex'],
                    'userAccount': self.mobile,
                    'verifyCode': self.config['verifycode']
                },
                self.config['accesstoken']
            )
        }
        resp = self.session.post(url=url, json=data)
        data = resp.json()
        print(data)
        data = data.get('data', {})
        log = f'{self.now_time}_ngworead_{data["prizeword"]}'
        self.recordLog(log)

    def queryUserPrizeRecords(self):
        url = 'https://10010.woread.com.cn/ng_woread_service/rest/activity/yearEnd/queryUserPrizeRecords'
        data = {
            'sign': encrypt(
                {
                    'curPage': 1,
                    'limit': 10,
                    'year': '',
                    'month': '',
                    'timestamp': self.formatTime,
                    'token': self.config['token'],
                    'userId': self.config['userid'],
                    'userIndex': self.config['userindex'],
                    'userAccount': self.mobile,
                    'verifyCode': self.config['verifycode']
                },
                self.config['accesstoken']
            )
        }
        resp = self.session.post(url=url, json=data)
        data = resp.json()
        print(data)
        return data.get('total', 0)

    def run(self):
        if int(self.now_date.replace('-', '')) > 20220228:
            return
        self.config = self.readCookie(f'{self.mobile}NGWoRead') or {}
        if not isinstance(self.config, dict) or self.config.get('t', '') != self.now_date \
                or not self.config.get('token', '') or not self.config.get('accesstoken', ''):
            self.getAccessToken()
            self.login()
        else:
            self.session.headers.update({
                'accesstoken': self.config['accesstoken']
            })
        self.config.update({'activeindex': self.queryActiveInfo()})
        for activeIndex in [6880]:
            if self.checkUserTakeActive(activeIndex):
                self.userTakeActive(activeIndex)
        # self.queryAdList()
        taskList = self.queryScoreWay()
        for task in taskList:
            if task['taskname'] == '看1次视频得20幸运值':
                gainnum = task['gainnum'] or 0
                daylimit = task['daylimit']
                for _ in range(0, daylimit - gainnum):
                    value = task['mapList'][0]['bindvalue']
                    self.obtainScoreByAd(value)
                    self.flushTime(randint(3, 5))
        validScore = self.queryUserScore()
        total = self.queryUserPrizeRecords()
        if total < 60:
            for _ in range(0, validScore // 50):
                self.handleDrawLottery()
                self.flushTime(randint(2, 3))


if __name__ == '__main__':
    pass
