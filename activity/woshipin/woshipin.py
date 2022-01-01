# -*- coding: utf8 -*-
import json
import requests
from random import randint, choice
from utils.unicomLogin import UnicomClient
from utils.mbh import random, gztoken


class WoShiPin(UnicomClient):

    def __init__(self, mobile, password):
        super(WoShiPin, self).__init__(mobile, password)
        self.session.cookies.clear_session_cookies()
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "Origin": "https://mbh.chinaunicomvideo.cn",
            "User-Agent": self.useragent,
            # "Content-Type": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "accept": "application/json, text/plain, */*",
            "Referer": "https://mbh.chinaunicomvideo.cn/wovideo/video/index.html",
            "X-Requested-With": "com.sinovatech.unicom.ui",
        })
        self.userId = random()
        self.physicalDeviceID = random()
        self.total = randint(7000, 8000) + round(randint(10, 99) / 100, 2)  # 7267.72

    @property
    def innerNetIp(self):
        return '%s.%s.%s.%s' % ('10', randint(1, 255), randint(1, 255), randint(1, 255))

    def loginRoute(self):
        url = 'https://mbh.chinaunicomvideo.cn/loginroute/EDS/V3/LoginRoute'
        data = {
            "userId": self.userId
        }
        resp = self.session.post(url=url, json=data, headers={
            'Content-Type': 'application/json;charset=UTF-8'
        })
        print(resp.json())

    def getToken(self):
        url = 'https://mbh.chinaunicomvideo.cn/GzUpload/h5/getToken'
        timestamp = (self.now_date + self.now_time).replace('-', '').replace(':', '')
        data = {
            "timestamp": timestamp,
            "md5": gztoken(self.mobile, timestamp),
            "mobile": self.mobile
        }
        resp = self.session.post(url=url, data=data)
        print(resp.json())

    def login(self):
        url = 'https://mbh.chinaunicomvideo.cn/VSP/V3/Login'
        data = {}
        resp = self.session.post(url=url, json=data, headers={
            'Content-Type': 'application/json;charset=UTF-8',
            'userid': str(self.userId)
        })
        print(resp.json())

    def Authenticate(self, retry=1):
        url = 'https://mbh.chinaunicomvideo.cn/VSP/V3/Authenticate'
        data = json.dumps({
            "authenticateBasic": {
                "userType": "0",
                "authType": 1,
                "userID": self.mobile,
                "clientPasswd": "wotv1596378"
            },
            "authenticateDevice": {
                "deviceModel": "Wotv_H5",
                "physicalDeviceID": self.physicalDeviceID
            },
            "authenticateTolerant": {
                "subnetID": "8601"
            }
        }, separators=(',', ':')).encode('utf8')
        resp = self.session.post(url=url, data=data, headers={
            'userid': str(self.userId)
        })
        print(resp.json())
        data = resp.json()
        if data.get('result', {}).get('retMsg', '').lower().find('password') > -1 and retry > 0:
            self.createUserForVR()
            self.Authenticate(retry - 1)
        else:
            self.saveCookie(
                f'{self.mobile}WoShiPin',
                {
                    'cookie': self.session.cookies.get_dict(),
                    't': self.now_date,
                    'userid': self.userId,
                    'physicalDeviceID': self.physicalDeviceID
                }
            )

    def createUserForVR(self):
        url = 'https://mbh.chinaunicomvideo.cn/GW/createUserForVR'
        data = {
            "userId": self.mobile
        }
        resp = self.session.post(url=url, json=data, headers={
            'Content-Type:application/json;charset=UTF-8'
        })
        print(resp.json())

    def QueryAllChannel(self):
        url = 'https://mbh.chinaunicomvideo.cn/VSP/V3/QueryAllChannel'
        data = {}
        resp = self.session.post(url=url, json=data, headers={
            'Content-Type': 'application/json;charset=UTF-8',
            'X_CSRFToken': self.session.cookies.get('CSRFSESSION', ''),
            'userid': str(self.userId)
        })
        data = resp.json()
        data = data.get('channelDetails', [])
        return choice([item['ID'] for item in data] or ['265428'])

    def saveUserAction(self, videoId, duration):
        url = 'https://mbh.chinaunicomvideo.cn/TjCenter/wovideo/wovideoWap/saveUserAction'
        data = {
            "projectName": "points",
            "mobile": self.mobile,
            "videoId": videoId,  # "265428",
            "videoType": "1",
            "channel": "",  # stjfk21
            "operate_id": "228",
            "operate_value": "{\"duration\":%s,\"total_duration\":\"%s\"}" % (duration, self.total),
            "platform": "Android|browser",
            "ip": self.innerNetIp,
            "pageUrl": f"https://mbh.chinaunicomvideo.cn/wovideo/video/index.html#/play?resourceId={videoId}",
            "channel": "",  # stjfk21
            "isSearch": "false",
            "yw_code": "",
            "desmobile": self.mobile,
            "version": self.version
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(data)
        return data.get('status', '1')

    def run(self):
        woshipin = self.readCookie(f'{self.mobile}WoShiPin')
        if not isinstance(woshipin, dict) or woshipin.get('t', '') != self.now_date or \
                not woshipin.get('userid', '') or not woshipin.get('cookie', {}).get('CSRFSESSION', '').strip(' "'):
            self.loginRoute()
            self.getToken()
            self.login()
            self.Authenticate()
        else:
            self.session.cookies.update(woshipin['cookie'])
            self.userId = woshipin['userid']
            self.physicalDeviceID = woshipin['physicalDeviceID']
        print(self.innerNetIp)
        if not self.session.cookies.get('CSRFSESSION', '').strip(' "'):
            raise Exception('[WoShiPin]登录失败,结束执行任务')
        videoId = self.QueryAllChannel()
        for duration in ['10', '1800', '3600', '5400']:
            if self.saveUserAction(videoId, duration) == '1':
                break
            self.flushTime(randint(3, 5))


if __name__ == '__main__':
    pass
