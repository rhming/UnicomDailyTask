# -*- coding: utf8 -*-
import requests
from utils.bol import encrypt_password
from utils import jsonencode as json
from utils.common import Common
import time


class WoMailWeb(Common):

    def __init__(self, mobile, password):
        super(WoMailWeb, self).__init__()
        self.mobile = mobile
        self.password = password
        self.session = requests.Session()
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "Referer": "https://club.mail.wo.cn/clubwebservice/club-user/user-info/sign-scope",
            "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; MI 8 SE Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36"
        })

    def accountLogin(self):
        url = 'https://account.bol.wo.cn/cuuser/cuauth/accountLogin'
        params = {
            'username': self.mobile,
            'password': encrypt_password(self.password),
            'clientId': 'userclub',
            'redirectUrl': 'https://club.mail.wo.cn/clubwebservice/club-user/user-info/sign-scope',
            'appType': '2',
            'state': ''
        }
        resp = self.session.post(url=url, params=params, json={}, headers={
            "Origin": "https://account.bol.wo.cn",
            "Referer": "https://account.bol.wo.cn/accountlogin?clientId=userclub&redirectUrl=null",
        })
        print(resp.headers)
        return resp.json().get('data', '')

    def cuuserLogin(self, url):
        if url:
            resp = self.session.get(url=url)
            cookies = resp.cookies.get_dict()
            self.saveCookie(f'{self.mobile}WoMailWeb', {
                'cookie': cookies,
                't': self.now_date
            })
        else:
            raise Exception('[WoMailWeb]登录失败 结束执行任务')

    def userSign(self):
        url = 'https://club.mail.wo.cn/clubwebservice/club-user/user-sign/create?channelId='
        resp = self.session.get(url=url)
        print(resp.json())

    def signRecord(self):
        url = 'https://club.mail.wo.cn/clubwebservice/club-user/user-sign/query-continuous-sign-record'
        resp = self.session.get(url=url)
        data = resp.json()
        print(json.dumps(data))
        try:
            data = data[0]
            return data['createDate'], data['newContinuousDay']
        except:
            return 0, 0

    def monthSignInfo(self):
        url = 'https://club.mail.wo.cn/clubwebservice/club-user/user-sign/month-sign-info'
        resp = self.session.get(url=url)
        data = resp.json()

    def queryGrowthTask(self):
        url = 'https://club.mail.wo.cn/clubwebservice/growth/queryGrowthTask'
        resp = self.session.get(url=url)
        data = resp.json()
        print(data)

    def queryIntegralTask(self):
        url = 'https://club.mail.wo.cn/clubwebservice/growth/queryIntegralTask?channelId=club'
        resp = self.session.get(url=url)
        data = resp.json()
        print(data)
        return data['data']

    def run(self):
        cookies = self.readCookie(f'{self.mobile}WoMailWeb')
        if not isinstance(cookies, dict) or cookies.get('t', '') != self.now_date or not cookies.get('cookie', ''):
            # print('开始登录')
            url = self.accountLogin()
            self.cuuserLogin(url)
        else:
            print(cookies)
            self.session.cookies.update(cookies['cookie'])
        createDate, newContinuousDay = self.signRecord()
        createDate = time.strftime('%Y-%m-%d', time.localtime(createDate / 1000))
        if createDate != self.now_date:
            print('未签到')
            self.userSign()
        else:
            print('已签到')

        # for task in self.queryIntegralTask():
        #     if task['resourceName'] in ['沃邮箱网页版登录']:
        #         if task['taskState'] == 0:
        #             # sid, key = self.getPasswordKey()
        #             # config = self.userLogin(sid, key)
        #             # sid = config['sid']
        #             print()
        # print()


if __name__ == '__main__':
    pass
