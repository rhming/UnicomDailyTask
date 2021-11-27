# -*- coding: utf8 -*-
import requests
from utils import jsonencode as json
from activity.womusic.womusic import WoMusic


class DayDayDraw(WoMusic):

    def __init__(self, mobile, password):
        super(DayDayDraw, self).__init__(mobile, password)
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "Origin": "https://m.10155.com",
            "User-Agent": self.useragent,
            # "content-type": "application/json",
            "content-type": "application/x-www-form-urlencoded",
            "accept": "application/json, text/plain, */*",
            "Referer": "https://m.10155.com/h5/crbt-huodong/daydaydraw.html",
            "X-Requested-With": "com.sinovatech.unicom.ui",
        })
        self.config = {}

    def openPlatLineNew(self, to_url, retry=3):
        try:
            url = f'https://m.client.10010.com/mobileService/openPlatform/openPlatLineNew.htm?to_url={to_url}'
            resp = self.session.get(url=url, allow_redirects=False)
            location = resp.headers['location']
            self.config = {
                kv.split('=', 1)[0]: kv.split('=', 1)[1] for kv in location.split('?', 1)[1].split('&') if kv.strip()
            }
            self.session.headers.update({
                'Referer': location
            })
            print(json.dumps(self.config))
            print(location)
        except Exception as e:
            print(e)
            if retry > 0:
                self.flushTime(5)
                self.openPlatLineNew(to_url, retry - 1)
            else:
                raise Exception("[WoMusic]获取登录配置失败, 结束执行任务")

    def getTicket(self):
        url = 'https://m.10155.com/woapp/h5/login/getTicket'
        resp = self.session.post(url=url)
        data = resp.json()
        return data.get('result', '')

    def getMobileByAppTicket(self, ticket):
        url = 'https://m.10155.com/ringplat/common/getMobileByAppTicket'
        data = {
            'ticket': self.config['ticket'],
            'sessionId': ticket,
            'activityName': 'DailyCredits',
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        self.session.headers.update({
            'sessionid': data.get('data', {}).get('sessionId', '')
        })

    def getMobileWithTicket(self, ticket):
        url = 'https://m.10155.com/ringplat/common/getMobileWithTicket'
        data = {
            'ticket': ticket
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        self.session.headers.update({
            'sessionid': data.get('data', {}).get('sessionId', '')
        })

    def lotteryRemainTimes(self):
        url = 'https://m.10155.com/ringplat/wo/luck/lotteryRemainTimes'
        data = {
            "phone": self.mobile,
            "activityName": "DailyCredits",
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(data)
        return data.get('data', {}).get('remainTimes', 0)

    def lottery(self):
        url = 'https://m.10155.com/ringplat/wo/luck/lottery'
        data = {
            'phone': self.mobile,
            'activityName': 'DailyCredits',
            'channelId': '3000007200'
        }
        resp = self.session.post(url=url, data=data)
        print(resp.json())

    def run(self):
        to_url = 'https://m.10155.com/h5/crbt-huodong/daydaydraw.html#/index?chl=3000007200'
        self.openPlatLineNew(to_url)
        self.session.cookies.clear_session_cookies()
        womusic = self.readCookie(f'{self.mobile}WoMusic')
        if not (isinstance(womusic, dict) and womusic.get('t', '') == self.now_date):
            code = self.getLoginCode()
            self.videoRingLogin(code)
        else:
            self.session.headers.update({
                "accessToken": womusic['accessToken']
            })
        ticket = self.getTicket()
        self.getMobileByAppTicket(ticket)
        self.getMobileWithTicket(ticket)
        for _ in range(self.lotteryRemainTimes()):
            self.lottery()
            self.flushTime(3)


if __name__ == '__main__':
    pass
