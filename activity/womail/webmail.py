# -*- coding: utf8 -*-
import requests
from utils.bol import encrypt_password
from utils import jsonencode as json
from utils.common import Common
import time


class WoMailWeb(Common):
    """
    club.mail.wo.cn
    club.soyu.cn
    """

    def __init__(self, mobile, password):
        super(WoMailWeb, self).__init__()
        self.mobile = mobile
        self.password = password
        self.session = requests.Session()
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "Referer": "https://club.soyu.cn/clubwebservice/club-user/user-info/sign-scope",
            "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; MI 8 SE Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36"
        })

    def accountLogin(self):
        url = 'https://account.bol.wo.cn/cuuser/cuauth/accountLogin'
        params = {
            'username': self.mobile,
            'password': encrypt_password(self.password),
            'clientId': 'userclub',
            'redirectUrl': 'https://club.soyu.cn/clubwebservice/club-user/user-info/sign-scope',
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
        url = 'https://club.soyu.cn/clubwebservice/club-user/user-sign/create?channelId='
        resp = self.session.get(url=url)
        print(resp.json())

    def signRecord(self):
        url = 'https://club.soyu.cn/clubwebservice/club-user/user-sign/query-continuous-sign-record'
        resp = self.session.get(url=url)
        data = resp.json()
        print(json.dumps(data))
        try:
            data = data[0]
            return data['createDate'], data['newContinuousDay']
        except:
            return 0, 0

    def monthSignInfo(self):
        url = 'https://club.soyu.cn/clubwebservice/club-user/user-sign/month-sign-info'
        resp = self.session.get(url=url)
        data = resp.json()

    def queryGrowthTask(self):
        url = 'https://club.soyu.cn/clubwebservice/growth/queryGrowthTask'
        resp = self.session.get(url=url)
        data = resp.json()
        print(data)
        return data['data']

    def queryIntegralTask(self):
        url = 'https://club.soyu.cn/clubwebservice/growth/queryIntegralTask?channelId=club'
        resp = self.session.get(url=url)
        data = resp.json()
        print(data)
        return data['data']

    def addIntegral(self, resourceFlag):
        url = 'https://club.soyu.cn/clubwebservice/growth/addIntegral'
        data = {'resourceType': resourceFlag, 'jumpToAdd': 'true'}
        resp = self.session.get(url=url, params=data)
        print(resp.json())

    def addGrowthViaTask(self, resourceFlag):
        url = 'https://club.soyu.cn/clubwebservice/growth/addGrowthViaTask'
        data = {'resourceType': resourceFlag, 'jumpToAdd': 'true'}
        resp = self.session.get(url=url, params=data)
        print(resp.json())

    def updateUserInfo(self):
        url = 'https://club.soyu.cn/clubwebservice/club-user/user-info/updateUserInfo'
        data = {
            "nickName": "--",
            "headPortrait": "/clubwebservice/static/user-login-false_03.jpg",
            "phoneNum": self.mobile,
            "sex": "男",
            "birthday": "--",
            "education": "",
            "vocation": "",
            "telephone": "",
            "zipCode": ""
        }
        resp = self.session.post(url=url, json=data, headers={
            'Content-Type': 'application/json;charset=UTF-8'
        })
        print(resp.json())

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

        for task in self.queryIntegralTask():
            if task['resourceName'] in ['沃邮箱网页版登录'] and task['taskState'] == 0:
                from activity.womail.mailxt5 import XT5CoreMail
                XT5CoreMail(self.mobile, self.password).run()
            else:
                if task['taskState'] == 0:
                    self.addIntegral(task['resourceFlag'])
                    print()
        for task in self.queryGrowthTask():
            if task['resourceName'] == '俱乐部修改个人资料' and task['taskState'] == 0:
                self.updateUserInfo()
            else:
                if task['taskState'] == 0:
                    self.addGrowthViaTask(task['resourceFlag'])
        print()


if __name__ == '__main__':
    pass
