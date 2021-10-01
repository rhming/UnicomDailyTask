# -*- coding: utf8 -*-
import requests
from random import randint
from utils import jsonencode as json
from utils.toutiao_reward import TouTiao
from utils.unicomLogin import UnicomClient


class SuperSimpleTask(UnicomClient):
    """
        签到页积分任务
    """

    def __init__(self, mobile, password):
        super(SuperSimpleTask, self).__init__(mobile, password)
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "accept": "application/json, text/plain, */*",
            "origin": "https://img.client.10010.com",
            "user-agent": self.useragent,
            "content-type": "application/x-www-form-urlencoded",
            "referer": "https://img.client.10010.com/SigininApp/index.html",
            "x-requested-with": "com.sinovatech.unicom.ui"
        })
        self.toutiao = TouTiao(mobile)

    def getTask(self, floorMark):
        url = 'https://act.10010.com/SigninApp/superSimpleTask/getTask'
        data = {
            'floorMark': floorMark  # superEasy bigRew
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        # print(json.dumps(data))
        return data['data']

    def doTask(self, item):
        print(item['title'])
        url = 'https://act.10010.com/SigninApp/simplyDotask/doTaskS'
        data = {
            'taskId': item['taskId']
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(json.dumps(data))

    def accomplishDotaskOptions(self):
        url = 'https://act.10010.com/SigninApp/simplyDotask/accomplishDotask'
        _ = self.session.options(url=url, headers={
            'Content-Type': 'application/json'
        })

    def accomplishDotask(self, item, orderId=''):
        url = 'https://act.10010.com/SigninApp/simplyDotask/accomplishDotask'
        data = {
            "taskId": item['taskId'],
            "systemCode": "QDQD",
            "orderId": orderId
        }
        resp = self.session.post(url=url, json=data, headers={
            'Content-Type': 'application/json'
        })
        data = resp.json()
        print(json.dumps(data))

    def receiveBenefits(self):
        url = 'https://act.10010.com/SigninApp/floorData/receiveBenefits'
        resp = self.session.post(url=url)
        data = resp.json()
        print(json.dumps(data))

    def energy(self):
        url = 'https://act.10010.com/SigninApp/simplyDotask/energy'
        resp = self.session.post(url=url)
        data = resp.json()
        print(json.dumps(data))

    def recordLog(self, log):
        record = self.readCookie(f'{self.mobile}SuperSimpleTaskRecord')
        if not record:
            record = {}
        if len(record) > 30:
            k = list(record.keys())[0]
            record.pop(k)
        record[self.now_date] = log
        self.saveCookie(f'{self.mobile}SuperSimpleTaskRecord', record)

    def run(self):

        for item in self.getTask('superEasy'):
            # return
            print(json.dumps(item))
            if item['title'] in [
                '去浏览积分商城', '兑换1次话费红包', '玩4次0元夺宝',
                '玩3次转盘赢好礼', '玩3次套牛赢好礼', '玩3次扔球赢好礼',
                '玩3次刮刮乐', '玩3次开心抓大奖', '看2次完整视频得积分'
            ] and int(item['achieve']) != int(item['allocation']) and item['btn'] not in ['倒计时']:
                print(item['title'])
                print(int(item['allocation']) - int(item['achieve']))
                for _ in range(int(item['allocation']) - int(item['achieve'])):
                    orderId = ''
                    self.accomplishDotaskOptions()
                    self.flushTime(1)
                    if item['title'] == '看2次完整视频得积分':
                        self.flushTime(randint(15, 20))
                        options = {
                            'arguments1': '',
                            'arguments2': '',
                            'codeId': 946779474,
                            'remark': '签到超简单任务看视频',
                            'channelName': '简单任务-看视频得奖励',
                            'ecs_token': self.session.cookies.get('ecs_token')
                        }
                        orderId = self.toutiao.reward(options)
                    self.accomplishDotask(item, orderId)
                    item['achieve'] = int(item['achieve']) + 1
                    self.flushTime(randint(10, 15))
                # self.flushTime(randint(60, 65))
                # break
            if int(item['achieve']) == int(item['allocation']) and item['btn'] not in ['已完成', '倒计时']:
                # int(item['showStyle']) != 3:
                self.doTask(item)
                self.receiveBenefits()
                self.flushTime(randint(10, 15))
                break
        for item in self.getTask('bigRew'):
            if int(item['achieve']) == int(item['allocation']) and item['btn'] != '已完成':  # int(item['showStyle']) != 3:
                self.doTask(item)
                self.flushTime(randint(5, 10))
        self.energy()

        self.flushTime(randint(3, 5))
        log = '[superEasy]\n'
        for item in self.getTask('superEasy'):
            log += f"{item['title']}:{item['btn']}---进度:{item['achieve']}/{item['allocation']}\n"
        log += '[bigRew]\n'
        for item in self.getTask('bigRew'):
            log += f"{item['title']}:{item['btn']}---进度:{item['achieve']}/{item['allocation']}\n"
        self.recordLog(log)


if __name__ == '__main__':
    pass
