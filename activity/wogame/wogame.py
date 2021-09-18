# -*- coding: utf8 -*-
import json
import time
import requests
from random import randint
from utils import root_pb2
from utils.qqmini_sdk import HmacSHA256
from utils.unicomLogin import UnicomClient
from utils.hb import heartbeat, getUrlParam
from google.protobuf import message, json_format


class WoGame(UnicomClient):

    def __init__(self, mobile, password):
        super(WoGame, self).__init__(mobile, password)
        self.clientVersion = self.version.split("@")[1]
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://img.client.10010.com",
            "User-Agent": self.useragent,
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": f"https://img.client.10010.com/gametask/index.html?yw_code=&desmobile={self.mobile}&version={self.version}",
            "X-Requested-With": "com.sinovatech.unicom.ui"
        })

    def gameVerify(self):
        jwt = self.session.cookies.get('jwt')
        url = 'https://m.client.10010.com/game/verify'
        data = {
            "extInfo": jwt,
            "auth": {
                "uin": self.mobile,
                "sig": jwt
            }
        }
        resp = self.session.post(url=url, json=data, headers={
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'okhttp/4.4.0'
        })
        print(resp.json())
        return resp.json()

    def clickRecord(self, gameId):
        url = 'https://m.client.10010.com/producGameApp'
        data = {
            "methodType": "record",
            "gameId": gameId,
            "deviceType": "Android",
            "taskId": "",
            "clientVersion": self.clientVersion
        }
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        print(resp.json())

    def iosTaskRecord(self, gameId):
        url = 'https://m.client.10010.com/producGameApp'
        data = {
            "methodType": "iOSTaskRecord",
            "gameId": gameId,
        }
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        print(resp.json())

    def qucikLogin(self, game_url, retry=3):
        """
            沃游戏登录
        """
        try:
            url = f'{game_url}&yw_code=&desmobile={self.mobile}&version={self.version}&ecsToken={self.session.cookies.get("ecs_token")}'
            resp = self.session.get(url=url, headers={
                "User-Agent": self.useragent,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Referer": f"{game_url}&yw_code=&desmobile={self.mobile}&version={self.version}",
                "X-Requested-With": "com.sinovatech.unicom.ui"
            })
            resp.encoding = 'utf8'
            cookie = resp.cookies.get_dict()  # type: dict
            print(json.dumps(cookie, indent=4, ensure_ascii=False))
            # etree.HTML(resp.text)
            if not cookie.get('stl_id', False) or not cookie.get('newid', False):
                raise Exception("[WoGame]获取登录cookie失败")
        except Exception as e:
            print(e)
            if retry > 0:
                self.flushTime(10)
                self.qucikLogin(game_url, retry - 1)
            else:
                raise Exception('[WoGame]登录失败, 结束执行任务')

    def reportedGame(self, game_url, retry=3):
        """
            沃游戏记录
        """
        try:
            newid = self.session.cookies.get("newid")
            gid = getUrlParam(game_url, "gid")
            stl_id = self.session.cookies.get("stl_id")
            sign, nonce, timestamp = heartbeat(newid, gid, stl_id)
            url = f'https://www.wostore.cn/woyoujiang/activity/game-report12?uid={newid}&gid={gid}&launchid={stl_id}&nonce={nonce}&timestamp={timestamp}&sign={sign}'
            resp = self.session.get(url=url, headers={
                "Origin": "http://assistant.flow.wostore.cn",
                "User-Agent": self.useragent,
                "Referer": f"{game_url}&xw_ltn={self.session.cookies.get('loginnew')}",
                "X-Requested-With": "com.sinovatech.unicom.ui"
            })
            print(resp.json())
        except Exception as e:
            print(e)
            if retry > 0:
                self.flushTime(10)
                self.reportedGame(game_url, retry - 1)
            else:
                print("沃游戏上报失败")

    def judgeTime(self, resourceId, minute, n):
        date_string = time.strftime(
            '%m%d%H%M%S',
            time.localtime(self.timestamp / 1000)
        )
        t = self.timestamp % 1000
        s = randint(0, 90000 - 1) + 10000
        traceid = f'{self.mobile}_{date_string}{t}_{s}'
        if not self.firsttime:
            self.firsttime = self.timestamp + 67056 * 1000
        self.reporttime.append(randint(60, 65))  # 55
        info = {
            'Seq': 3 if n == 1 else 13 + n,
            'qua': 'V1_AND_MINISDK_1.5.4_0_RELEASE_B',
            'deviceInfo': "m=MI 8 SE&o=8.1.0&a=27&p=2134*1080&f=Xiaomi&mm=5679&cf=1668&cc=8&qqversion=null",
            'busiBuff': {
                'extInfo': {
                    'attachInfo': '0'
                },
                'appid': resourceId,
                'factType': 13 if n == minute else 12,  # 11 12 13
                'duration': 0,
                'reportTime': self.server_timestamp // 1000,
                'afterCertify': 0,
                'appType': 1,
                'scene': 1001,
                'totalTime': sum(self.reporttime),
                'launchId': str(self.firsttime),
                'via': '',
                'AdsTotalTime': 0,
                'hostExtInfo': ''
            },
            'traceid': traceid,
            'Module': 'mini_app_growguard',
            'Cmdname': 'JudgeTiming',
            'loginSig': {
                'uin': self.mobile,
                'sig': self.session.cookies.get('jwt'),
                'platform': '2001',
                'type': 0,
                'appid': '101794394'
            },
            'Crypto': None,
            'Extinfo': None,
            'contentType': 0,
        }
        JudgeTimingBusiBuff = root_pb2.nested().JudgeTimingBusiBuff()  # type: message.Message
        JudgeTimingBusiBuff = json_format.ParseDict(info, JudgeTimingBusiBuff)
        data = JudgeTimingBusiBuff.SerializeToString()
        timestamp = self.timestamp // 1000
        nonce = randint(-2 ** 31, 2 ** 31 - 1)
        request_url = f'POST /mini/OpenChannel?Action=input&Nonce={nonce}&PlatformID=2001&SignatureMethod=HmacSHA256&Timestamp={timestamp}'
        signature = HmacSHA256(request_url)
        url = f'https://q.qq.com/mini/OpenChannel?Action=input&Nonce={nonce}&PlatformID=2001&SignatureMethod=HmacSHA256&Timestamp={timestamp}&Signature={signature}'
        resp = self.session.post(url=url, data=data, headers={
            "user-agent": "okhttp/4.4.0"
        })
        resp.encoding = 'utf8'
        print(resp.content)
