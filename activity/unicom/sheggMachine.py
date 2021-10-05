# -*- coding: utf8 -*-
# import json
import re
import requests
from random import randint
from utils import jsonencode as json
from utils.toutiao_reward import TouTiao
from utils.unicomLogin import UnicomClient
from utils.jifen import encrypt_req_params, encrypt_free_login_params


class SheggMachine(UnicomClient):

    def __init__(self, mobile, password):
        super(SheggMachine, self).__init__(mobile, password)
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "origin": "https://m.jf.10010.com",
            "user-agent": self.useragent,
            "content-type": "application/json",
            "accept": "*/*",
            "referer": "https://m.jf.10010.com/cms/yuech/unicom-integral-ui/shegg-machine/index.html?id=Ac-f4557b3ac6004a48b1187e32ea343ca8&jump=sign",
        })
        self.clientVersion = self.version.split('@')[1]
        self.toutiao = TouTiao(mobile)
        self.activityId = 'Ac-f4557b3ac6004a48b1187e32ea343ca8'

    # def getUrlParam(self, name, value):
    #     # 'Ac-f4557b3ac6004a48b1187e32ea343ca8'
    #     return re.findall(name + r'=([^&]+)', value)[0]

    def openPlatLineNew(self, to_url, retry=3):
        try:
            url = f'https://m.client.10010.com/mobileService/openPlatform/openPlatLineNew.htm?to_url={to_url}'
            _ = self.session.get(url=url, headers={
                "Origin": "https://img.client.10010.com",
                "X-Requested-With": "com.sinovatech.unicom.ui"
            })
            # self.global_config['cookie'] = self.session.cookies.get_dict()
            # self.global_config['cookie']['_jf_t'] = str(self.timestamp)
            # self.saveCookie(f'{self.mobile}WoGame', self.global_config)
            if not self.session.cookies.get('_jf_id', ''):
                raise Exception('未获取到_jf_id')
        except Exception as e:
            print(e)
            if retry > 0:
                self.flushTime(5)
                self.openPlatLineNew(to_url, retry - 1)
            else:
                raise Exception("[SheggMachine]获取登录配置失败, 结束执行任务")

    def freeLoginRock(self):
        url = 'https://m.jf.10010.com/jf-yuech/p/freeLoginRock'
        data = {
            'activityId': self.activityId,
            'userCookie': self.session.cookies.get('_jf_id'),
            'userNumber': self.mobile,
            'time': self.timestamp
        }
        data = encrypt_free_login_params(data)
        # print(data)
        # return
        resp = self.session.post(url=url, json=data)
        data = resp.json()
        print(json.dumps(data))
        token = data['data']['token']  # type: dict
        token.update({"t": self.now_date})
        # token.update({
        #     'activityInfos': data['data']['activityInfos']['activityVOs'][0]['activityTimesInfo']
        # })
        self.saveCookie(f'{self.mobile}JFToken', token)
        self.session.headers.update({
            "authorization": f"Bearer {token['access_token']}"
        })
        return token

    def minusGameTimes(self, params, token={}, retry=1):
        url = 'https://m.jf.10010.com/jf-yuech/api/gameResultV2/minusGameTimes'
        data = {
            'params': encrypt_req_params(params, self.session.cookies.get('_jf_id'))
        }
        resp = self.session.post(url=url, json=data)
        try:
            data = resp.json()
            print(json.dumps(data))
            # token['activityInfos']['advertTimes'] = data['data']['advertTimes']
            # token['activityInfos']['freeTimes'] = data['data']['freeTimes']
            # self.saveCookie(f'{self.mobile}JFToken', token)
            return data['data']['resultId'], data['data']['freeTimes'], data['data']['advertTimes']
        except:
            if retry > 0:
                self.freeLoginRock()
                return self.minusGameTimes(params, token, retry - 1)
            return

    def luckDrawForPrize(self, resultId):
        url = 'https://m.jf.10010.com/jf-yuech/api/gameResultV2/luckDrawForPrize'
        data = {
            'params': encrypt_req_params({
                'activityId': self.activityId,
                'resultId': resultId  # 'Ga-16d4aa3caa3040e88c276db953a0464c'
            }, self.session.cookies.get('_jf_id'))
        }
        resp = self.session.post(url=url, json=data)
        data = resp.json()
        print(json.dumps(data))

    def numIntegralQuery(self):
        url = 'https://m.jf.10010.com/jf-yuech/api/integralLogs/numIntegralQuery'
        params = {
            'activityId': self.activityId,
            'serviceNo': self.mobile,
            'userType': 0
        }
        resp = self.session.get(url=url, params=params)
        data = resp.json()
        print(json.dumps(data))
        return data

    def run(self):
        to_url = f'https://m.jf.10010.com/jf-order/avoidLogin/forActive/lkmh&yw_code=&desmobile={self.mobile}&version={self.version}'
        self.openPlatLineNew(to_url)
        token = self.readCookie(f'{self.mobile}JFToken')
        if (
                not isinstance(token, dict)
                or token.get('t', '') != self.now_date
                or not token.get('access_token', '')
                # or not token.get('activityInfos', '')
        ):
            token = self.freeLoginRock()
        self.session.headers.update({
            "authorization": f"Bearer {token['access_token']}"
        })
        params = {
            'activityId': self.activityId,
            'currentTimes': 1,
            'type': '免费'
        }
        resultId, freeTimes, advertTimes = self.minusGameTimes(params)
        if advertTimes == 0:
            print('机会已用完')
            return
        if freeTimes == 1:
            # params = {
            #     'activityId': self.activityId,
            #     'currentTimes': 1,
            #     'type': '免费'
            # }
            # resultId, _, __ = self.minusGameTimes(params)
            if resultId:
                self.luckDrawForPrize(resultId)
        else:
            options = {
                'arguments1': 'AC20200611152252',
                'arguments2': '',
                'codeId': 945535633,
                'channelName': 'android-签到小游戏乐开盲盒-激励视频',
                'remark': '签到小游戏翻倍得积分',
                'ecs_token': self.session.cookies.get('ecs_token')
            }
            orderId = self.toutiao.reward(options)
            params = {
                'activityId': self.activityId,
                'currentTimes': advertTimes,
                'type': '广告',
                'orderId': orderId,
                'phoneType': 'android',
                'version': round(float(self.clientVersion), 4)
            }
            resultId, _, __ = self.minusGameTimes(params)
            if resultId:
                self.luckDrawForPrize(resultId)


if __name__ == '__main__':
    pass
