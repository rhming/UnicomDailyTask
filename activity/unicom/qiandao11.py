# -*- coding: utf8 -*-
# import json
import requests
from utils import jsonencode as json
from utils.unicomLogin import UnicomClient
from utils.jifen import encrypt_req_params, encrypt_free_login_params


class QianDao11(UnicomClient):

    def __init__(self, mobile, password):
        super(QianDao11, self).__init__(mobile, password)
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "origin": "https://m.jf.10010.com",
            "user-agent": self.useragent,
            "content-type": "application/json",
            "accept": "*/*",
            "referer": "https://m.jf.10010.com/cms/yuech/activity/dbe/index.html",
        })
        self.clientVersion = self.version.split('@')[1]
        self.activityId = 'Ac-jgg2'

    def openPlatLineNew(self, to_url, retry=3):
        try:
            url = f'https://m.client.10010.com/mobileService/openPlatform/openPlatLineNew.htm?to_url={to_url}'
            _ = self.session.get(url=url, headers={
                "Origin": "https://img.client.10010.com",
                "X-Requested-With": "com.sinovatech.unicom.ui"
            })
            if not self.session.cookies.get('_jf_id', ''):
                raise Exception('未获取到_jf_id')
        except Exception as e:
            print(e)
            if retry > 0:
                self.flushTime(5)
                self.openPlatLineNew(to_url, retry - 1)
            else:
                raise Exception("[QianDao11]获取登录配置失败, 结束执行任务")

    def freeLoginRock(self):
        url = 'https://m.jf.10010.com/jf-yuech/p/qiandao11/login'
        data = {
            # 'activityId': self.activityId,
            'userCookie': self.session.cookies.get('_jf_id'),
            'userNumber': self.mobile,
            # 'time': self.timestamp
        }
        data = encrypt_free_login_params(data)
        resp = self.session.post(url=url, json=data)
        data = resp.json()
        token = data['data']  # type: dict
        self.session.headers.update({
            "authorization": f"Bearer {token['access_token']}"
        })
        task = [item for item in data['data']['task']['qiandao'] if item['isDangtian'] == 'true'] or [{}]
        tiaozhan = data['data']['task'].get('tiaozhan', {})
        """
        [{'isDangtian': 'true', 'jifen': '10+', 'id': 2, 'isQiandao': 'true'}]
        {'wanchengCount': 1, 'value': 300, 'key': 14, 'status': '0'}
        """
        return task[0], tiaozhan

    def getActivity(self):
        url = 'https://m.jf.10010.com/jf-yuech/api/gameResultV2/getActivitys?activityIds=Ac-jgg2'
        resp = self.session.get(url=url)
        data = resp.json()
        try:
            return data['data']['activityVOs'][0]['activityTimesInfo']['freeTimes']
        except:
            return 0

    def startQianDao(self):
        url = 'https://m.jf.10010.com/jf-yuech/p/qiandao11/api/startQiandao'
        data = {
            "activityId": "Ac-leijiqiandao2"
        }
        resp = self.session.post(url=url, json=data)
        data = resp.json()
        print(data)

    def startTiaoZhan(self):
        url = 'https://m.jf.10010.com/jf-yuech/p/qiandao11/api/startTiaoZhan'
        data = {
            "activityId": "Ac-leijiqiandao2",
            "dayTime": 14
        }
        resp = self.session.post(url=url, json=data)
        print(resp.json())

    def minusGameTimes(self, params):
        url = 'https://m.jf.10010.com/jf-yuech/api/gameResultV2/minusGameTimes'
        data = {
            'params': encrypt_req_params(params, self.session.cookies.get('_jf_id'))
        }
        resp = self.session.post(url=url, json=data)
        try:
            data = resp.json()
            print(data)
            return data['data']['resultId'], data['data']['freeTimes'], data['data']['advertTimes']
        except:
            pass

    def luckDrawForPrize(self, resultId):
        url = 'https://m.jf.10010.com/jf-yuech/api/gameResultV2/luckDrawForPrize'
        data = {
            'params': encrypt_req_params({
                'activityId': self.activityId,
                'resultId': resultId
            }, self.session.cookies.get('_jf_id'))
        }
        resp = self.session.post(url=url, json=data)
        data = resp.json()
        print(json.dumps(data))

    def run(self):
        to_url = f'https://m.jf.10010.com/jf-order/avoidLogin/forActive/dbeo&yw_code=&desmobile={self.mobile}&version={self.version}'
        self.openPlatLineNew(to_url)
        task, tiaozhan = self.freeLoginRock()
        if task.get('isQiandao', 'true') == 'false':
            self.startQianDao()
        if tiaozhan.get('wanchengCount', -1) == -1:
            self.startTiaoZhan()
        if self.getActivity():
            params = {
                'activityId': 'Ac-jgg2',
                'currentTimes': 1,
                'type': '免费'
            }
            resultId, freeTimes, advertTimes = self.minusGameTimes(params)
            if resultId:
                self.luckDrawForPrize(resultId)


if __name__ == '__main__':
    pass
