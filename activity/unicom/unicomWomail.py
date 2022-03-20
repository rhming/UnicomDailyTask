# -*- coding: utf8 -*-
# import json
import re
import requests
from random import randint, randrange
from utils import jsonencode as json
from utils.toutiao_reward import TouTiao
from utils.unicomLogin import UnicomClient
from utils.jifen import encrypt_req_params, encrypt_free_login_params
from urllib import parse


class DailyWomail(UnicomClient):
    def __init__(self, mobile, password):
        super(DailyWomail, self).__init__(mobile, password)
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "user-agent": self.useragent,
            "X-Requested-With": "com.sinovatech.unicom.ui"
        })
        self.toutiao = TouTiao(mobile)

    def openPlatLineNew(self, to_url):
        info = None
        url = f'https://m.client.10010.com/mobileService/openPlatform/openPlatLineNew.htm?to_url={to_url}'
        headers = {
            "Origin": "https://img.client.10010.com",
        }
        resp = self.session.get(
            url=url, headers=headers, allow_redirects=False)
        # print(resp.status_code)
        # print(resp.headers)
        if not resp.status_code == 302:
            return info
        url = resp.headers['Location']
        resp = self.session.get(
            url=url, headers=headers, allow_redirects=False)
        # print(resp.status_code)
        # print(resp.headers)
        if not resp.status_code == 302:
            return info

        url = resp.headers['Location']
        url = parse.unquote(url)
        # 'https://womail.richpush.cn/cn/lottery/wap/index.html?mobile=khVmIRIT8EA6JncSqolrSg==&redirectUrl=https://mail.wo.cn/coremail/cmcu_addon/sso_redirect.jsp?sid=HAIVeoSSLYYgqXICdExfoeXzHdYDxDkh&url=https://mail.wo.cn/coremail/hxphone/sso.html#/frame/folder/1?sid=HAIVeoSSLYYgqXICdExfoeXzHdYDxDkh'
        p = '^(?P<url>[^?]+)\?mobile=(?P<mobile>.+)&redirectUrl=(?P<redirectUrl>.+)&url=(?P<url1>.+)$'
        m = re.match(p, url)
        if not m:
            return info
        info = m.groupdict()
        resp = self.session.get(
            url=url, headers=headers, allow_redirects=False)
        print(resp.status_code)
        print(resp.headers)
        info.update({'url': url})
        return info

    def loginCallback(self, info):
        headers = {
            "referer": info['url'],
        }
        data = {'mobile': info['mobile']}
        data = parse.urlencode(data)
        url = f'https://womail.richpush.cn/cn/lottery/login/callback.do?{data}'
        resp = self.session.get(
            url=url, data=data, headers=headers)
        # print(resp.status_code)
        # print(resp.headers)
        print(resp.content)

    def userInfo(self, info):
        headers = {
            "referer": info['url'],
        }
        url = f'https://womail.richpush.cn/cn/lottery/login/userInfo.do'
        resp = self.session.get(
            url=url, headers=headers)
        # print(resp.status_code)
        # print(resp.headers)
        data = resp.json()
        print(json.dumps(data, ensure_ascii=False, indent=2))

    def chance(self, info):
        headers = {
            "referer": info['url'],
        }
        url = f'https://womail.richpush.cn/cn/lottery/user/chance.do'
        resp = self.session.get(
            url=url, headers=headers)
        # print(resp.status_code)
        # print(resp.headers)
        data = resp.json()
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return data['result']

    def overtask(self, info):
        headers = {
            "referer": info['url'],
        }
        url = f'https://womail.richpush.cn/cn/lottery/user/overtask.do'
        resp = self.session.get(
            url=url, headers=headers)
        # print(resp.status_code)
        # print(resp.headers)
        data = resp.json()
        print(json.dumps(data, ensure_ascii=False, indent=2))
        over_tasks = []
        for task in data['result']:
            over_tasks.append(task['taskName'])
        return over_tasks

    def start(self, info):
        headers = {
            "referer": info['url'],
        }
        url = f'https://womail.richpush.cn/cn/lottery/user/start.do'
        resp = self.session.get(
            url=url, headers=headers)
        # print(resp.status_code)
        # print(resp.headers)
        data = resp.json()
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return data['result']

    def end(self, info):
        headers = {
            "referer": info['url'],
        }
        data = {'score': randrange(250, 400, 10)}
        data = parse.urlencode(data)
        url = f'https://womail.richpush.cn/cn/lottery/user/end.do?{data}'
        resp = self.session.get(
            url=url, headers=headers)
        # print(resp.status_code)
        # print(resp.headers)
        data = resp.json()
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return data['result']

    def lotteryDraw(self, info):
        headers = {
            "referer": info['url'],
        }
        url = f'https://womail.richpush.cn/cn/lottery/draw/draw.do'
        resp = self.session.get(
            url=url, headers=headers)
        # print(resp.status_code)
        # print(resp.headers)
        data = resp.json()
        print(json.dumps(data, ensure_ascii=False, indent=2))
        if data['result']['prizeTitle']:
            prize = data['result']['prizeTitle']
            self.recordLog(f'{prize}')

    def doTask(self, info, taskname):
        headers = {
            "referer": info['url'],
        }
        data = {'taskName': taskname}
        data = parse.urlencode(data)
        url = f'https://womail.richpush.cn/cn/lottery/user/doTask.do?{data}'
        resp = self.session.get(
            url=url, headers=headers)
        # print(resp.status_code)
        # print(resp.headers)
        data = resp.json()
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return data['result']

    def run(self):
        to_url = f'https://user.mail.wo.cn/cu-email/mobile/jump/1'
        info = self.openPlatLineNew(to_url)
        print(info)
        if not info:
            return
        self.loginCallback(info)
        self.userInfo(info)
        chance = self.chance(info)
        for i in range(chance):
            self.start(info)
            self.flushTime(randrange(25, 30))
            self.end(info)
            self.flushTime(1)
            self.lotteryDraw(info)
        over_tasks = self.overtask(info)
        for task in ["loginmail", "knowmail", "wodisk", "orderbill", "guide"]:
            if task in over_tasks:
                print(f'{task}已完成!')
                continue
            print(f'{task}进行中...')
            self.doTask(info, task)
            self.flushTime(randrange(3, 10))
            chance = self.chance(info)
            for i in range(chance):
                self.start(info)
                self.flushTime(randrange(25, 30))
                self.end(info)
                self.flushTime(1)
                self.lotteryDraw(info)


if __name__ == '__main__':
    pass
