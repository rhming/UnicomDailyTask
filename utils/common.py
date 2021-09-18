import time
import json
import requests
from random import choices
from utils.config import data_storage_server_url, Authorization


class Common(object):

    def __getattribute__(self, name, *args, **kwargs):
        obj = super().__getattribute__(name)
        if type(obj).__name__ == 'method':
            print(obj.__name__.center(64, '#'), self.mobile)
        return obj

    def __init__(self):
        self.mobile = ''

    @property
    def timestamp(self):
        return int((time.time() + 8 * 60 * 60) * 1000)

    @property
    def server_timestamp(self):
        return int(time.time() * 1000)

    @property
    def now_date(self):
        return time.strftime(
            '%Y-%m-%d', time.localtime(self.timestamp / 1000)
        )

    @property
    def now_time(self):
        return time.strftime(
            '%X', time.localtime(self.timestamp / 1000)
        )

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

    def flushTime(self, timeout):
        for _ in range(timeout, -1, -1):
            time.sleep(1)

    def readCookie(self, key, retry=5):
        """
            可能出现网络波动 增加重试请求
        """
        if not data_storage_server_url:
            raise Exception('数据存储接口错误')
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
        if data_storage_server_url.find('http') == -1:
            raise Exception('数据存储接口错误')
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
            result['data'] = '...'
            print(result)
        except Exception as e:
            print('saveCookie', e)
            if retry > 0:
                self.flushTime(5)
                return self.saveCookie(key, value, retry - 1)
            else:
                print("保存Cookie失败")
