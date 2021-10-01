# -*- coding: utf8 -*-
# import json
import time
import requests
from utils import jsonencode as json
from utils.toutiao_reward import TouTiao
from utils.unicomLogin import UnicomClient


class WoLearn(UnicomClient):

    def __init__(self, mobile, password):
        super(WoLearn, self).__init__(mobile, password)
        self.session.headers = requests.structures.CaseInsensitiveDict({
            'User-Agent': self.useragent,
            'Origin': 'https://edu.10155.com',
            'Referer': 'https://edu.10155.com/',
            'x-requested-with': 'com.sinovatech.unicom.ui'
        })
        self.toutiao = TouTiao(mobile)
        self.allconfig = self.readCookie(self.mobile + "WoLearn")
        if not self.allconfig:
            self.allconfig = {}

    def openPlatLineNew(self, to_url, retry=3):
        try:
            url = f'https://m.client.10010.com/mobileService/openPlatform/openPlatLineNew.htm?to_url={to_url}'
            resp = self.session.get(url=url, allow_redirects=False)
            location = resp.headers['location']
            config = {
                kv.split('=', 1)[0]: kv.split('=', 1)[1] for kv in location.split('?', 1)[1].split('&') if kv.strip()
            }
            config.update({
                'Referer': location
            })
            self.allconfig.update({
                config['chc']: config
            })
            print(json.dumps(config, indent=4, ensure_ascii=False))
            print(location)
            self.index(location)
        except Exception as e:
            print(e)
            if retry > 0:
                self.flushTime(5)
                self.openPlatLineNew(to_url, retry - 1)
            else:
                raise Exception("[WoLearn]获取登录配置失败, 结束执行任务")

    def recordPrize(self, reward_name):
        record = self.readCookie(self.mobile + "WoLearnRecord")
        if not record:
            record = {}
        if not record.get(self.now_date, False):
            if len(record) > 30:
                k = list(record.keys())[0]
                record.pop(k)
            record[self.now_date] = [reward_name]
        else:
            record[self.now_date].append(reward_name)
        self.saveCookie(self.mobile + "WoLearnRecord", record)

    def index(self, url):
        self.session.get(url=url)
        self.session.headers.update({
            'Referer': url
        })

    def shoutingTicketLogin(self, chc, retry=3):
        try:
            self.session.headers.update({
                'chc': chc,
                'jrplatform': '2',
                'x-requested-with': 'XMLHttpRequest',
                'content-type': 'application/x-www-form-urlencoded'
            })
            url = 'https://edu.10155.com/wxx-api/Api/Shouting/shoutingTicketLogin'
            data = {
                "p": "",
                "chc": chc,
                "jrPlatform": "ACTIVITY",
                "ua": self.useragent.replace(" ", "+"),
                "cookie": "",
                "ticket": self.allconfig[chc]['ticket'],
                "accountID": self.mobile,
                "shoutingversion": self.version
            }
            resp = self.session.post(url=url, data=data)
            resp.encoding = 'utf8'
            result = resp.json()
            print(json.dumps(result, indent=4, ensure_ascii=False))
            self.session.headers.update({
                'accessToken': result['data']['accessToken']
            })
            self.allconfig[chc].update({
                'accessToken': result['data']['accessToken']
            })
            self.saveCookie(self.mobile + "WoLearn", self.allconfig)
        except Exception as e:
            print(e)
            if retry > 0:
                self.flushTime(5)
                self.shoutingTicketLogin(chc, retry - 1)
            else:
                raise Exception("[WoLearn]登录失败, 结束执行任务")


if __name__ == '__main__':
    pass
