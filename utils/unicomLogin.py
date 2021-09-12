# -*- coding: utf8 -*-
import time
import json
import execjs
import requests
from random import choices
from utils.config import BASE_DIR, data_storage_server_url, Authorization


class UnicomClient(object):

    def __getattribute__(self, name, *args, **kwargs):
        obj = super().__getattribute__(name)
        if type(obj).__name__ == 'method':
            print(obj.__name__.center(64, '#'), self.mobile)
        return obj

    def __init__(self, mobile, password):

        self.mobile = mobile
        self.password = password
        self.version = "android@8.0805"
        self.deviceId = "" or self.getDeviceId
        self.useragent = "Mozilla/5.0 (Linux; Android 8.1.0; MI 8 SE Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36; unicom{version:%s,desmobile:%s};devicetype{deviceBrand:Xiaomi,deviceModel:MI 8 SE};{yw_code:}" % (
            self.version,
            self.mobile,
        )

        self.session = requests.Session()
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "okhttp/4.4.0"
        })
        self.global_config = self.readCookie(self.mobile + "WoGame")
        if not self.global_config:
            self.login()
        else:
            self.session.cookies.update(self.global_config['cookie'])
        if not (self.session.cookies.get('jwt', False) and self.session.cookies.get('ecs_token', False)):
            raise Exception('[UnicomClient]未登录状态')
        self.last_login_time = time.strftime(
            "%Y-%m-%d",
            time.localtime(
                int(self.global_config['online']['reqtime']) / 1000
            )
        )

    @property
    def timestamp(self):
        return int((time.time() + 8 * 60 * 60) * 1000)

    @property
    def server_timestamp(self):
        return int(time.time() * 1000)

    @property
    def getDeviceId(self):
        value = '86' + ''.join(choices('0123456789', k=12))
        sum_ = 0
        parity = 15 % 2
        for i, digit in enumerate([int(x) for x in value]):
            if i % 2 == parity:
                digit *= 2
                if digit > 9:
                    digit -= 9
            sum_ += digit
        value += str((10 - sum_ % 10) % 10)
        return value

    def onLineConf(self, item):
        return {
            "reqtime": str(self.timestamp),
            "provinceChanel": "general",
            "appId": self.getAppId(),
            "netWay": "4G",
            "deviceModel": "MI 8 SE",
            "step": "dingshi",
            "deviceCode": self.deviceId,
            "version": self.version,
            "deviceId": self.deviceId,
            "deviceBrand": "Xiaomi",
            "token_online": item['token_online']
        }

    def flushTime(self, timeout):
        for _ in range(timeout, -1, -1):
            time.sleep(1)

    def getAppId(self):
        with open(BASE_DIR + '/utils/appId.json', 'r', encoding='utf8') as fp:
            appIds = json.loads(fp.read())  # type: dict
        if not appIds.get(self.mobile, False):
            raise Exception('[UnicomClient]获取appId失败')
        return appIds.get(self.mobile)

    def readCookie(self, key, retry=5):
        """
            可能出现网络波动 增加重试请求
        """
        try:
            resp = requests.get(
                url=data_storage_server_url,
                params={"key": key},
                headers={
                    "Authorization": Authorization,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
                }
            )
            result = resp.json()
            if result["msg"]:
                data = result["data"]
                return data[key]
            else:
                return ''
        except Exception as e:
            print('readCookie', e)
            if retry > 0:
                self.flushTime(5)
                return self.readCookie(key, retry - 1)
            else:
                print("读取Cookie失败")
                return ''

    def saveCookie(self, key: str, value, retry=5):
        """
            可能出现网络波动 增加重试请求
        """
        try:
            if type(value) in [dict, list, tuple]:
                value = json.dumps(value, indent=4, ensure_ascii=False)
            # if not isinstance(value, str):
            #     value = str(value)
            resp = requests.post(
                url=data_storage_server_url,
                data={
                    "key": key,
                    "value": value
                },
                headers={
                    "Authorization": Authorization,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
                }
            )
            result = resp.json()
            result['extra'] = '...'
            print(result)
        except Exception as e:
            print('saveCookie', e)
            if retry > 0:
                self.flushTime(5)
                return self.saveCookie(key, value, retry - 1)
            else:
                print("保存Cookie失败")

    def JSEncrypt(self, message):
        with open(BASE_DIR + '/utils/unicom.js', 'r', encoding='utf8') as fp:
            js = fp.read()
        ctx = execjs.compile(js)
        result = ctx.call('RSAEncrypt', message)
        return result

    def checklogin(self):
        url = 'https://m.client.10010.com/mobileService/checklogin.htm'
        resp = self.session.get(url=url)
        result = resp.json()
        print(result)
        return result.get('islogin', False)

    def login(self):
        self.session.cookies.clear_session_cookies()
        for k in self.session.cookies.get_dict():
            self.session.cookies.pop(k)
        url = 'https://m.client.10010.com/mobileService/login.htm'
        data = {
            "simCount": "1",
            "yw_code": "",
            "deviceOS": "android8.1.0",
            "mobile": self.JSEncrypt(self.mobile),
            "netWay": "4G",
            "deviceCode": self.deviceId,
            "isRemberPwd": "true",
            "version": self.version,
            "deviceId": self.deviceId,
            "password": self.JSEncrypt(self.password),
            "keyVersion": "",
            "pip": "10." + '.'.join([str(v) for v in choices(range(1, 255), k=3)]),
            "provinceChanel": "general",
            "appId": self.getAppId(),
            "deviceModel": "MI 8 SE",
            "deviceBrand": "Xiaomi",
            "timestamp": time.strftime('%Y%m%d%H%M%S', time.localtime(self.timestamp / 1000))
        }
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        result = resp.json()
        if result.get('token_online', False):
            self.global_config['online'] = {
                "token_online": result['token_online'],
                "reqtime": str(self.timestamp)
            }
            self.global_config['cookie'] = self.session.cookies.get_dict()
            self.saveCookie(self.mobile + "WoGame", self.global_config)
        else:
            print(resp.text)

    def onLine(self):
        self.session.cookies.clear_session_cookies()
        for k in self.session.cookies.get_dict():
            self.session.cookies.pop(k)
        url = 'https://m.client.10010.com/mobileService/onLine.htm'
        data = self.onLineConf(self.global_config['online'])
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        result = resp.json()
        if result.get('token_online', False):
            self.global_config['online'] = {
                "token_online": result['token_online'],
                "reqtime": str(self.timestamp)
            }
            self.global_config['cookie'] = self.session.cookies.get_dict()
            self.saveCookie(self.mobile + "WoGame", self.global_config)
        else:
            print(resp.text)


if __name__ == '__main__':
    pass
