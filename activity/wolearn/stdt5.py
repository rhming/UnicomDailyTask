# -*- coding: utf8 -*-
# import json
from random import randint
from utils import jsonencode as json
from activity.wolearn.wolearn import WoLearn


class Stdthd(WoLearn):

    def __init__(self, mobile, password):
        super(Stdthd, self).__init__(mobile, password)
        self.chc = "CC1XJwYxUCkHYgx1V2MGO1NjUitXOg"
        self.config = self.allconfig.get(self.chc, {})
        if self.config.get('accessToken', False):
            self.session.headers.update({
                'accessToken': self.config['accessToken'],
                'Referer': self.config['Referer']
            })
            self.isLogin = True
        else:
            self.isLogin = False
        self.prizeList = []
        self.actId = '5'

    def getReward(self, item):
        url = 'https://edu.10155.com/wxx-api/Api/Stdthd/getReward'
        data = {
            "p": "",
            "chc": self.config.get('chc'),
            "jrPlatform": "ACTIVITY",
            "ua": self.useragent.replace(" ", "+"),
            "cookie": "",
            "bonusId": item['sbl_id'],  # "_this.receiveReward.zbl_id",
            "account": self.mobile
        }
        if item['sbl_reward_log']:
            data["extra"] = {
                "name": "",
                "phone": self.mobile,
                "addr": ""
            }
            # TODO
            return
        resp = self.session.post(url=url, data=data)
        result = resp.json()
        print(result)

    def raffle(self, sal_id):
        url = 'https://edu.10155.com/wxx-api/Api/Stdthd/raffle'
        data = {
            "p": "",
            "chc": self.config.get('chc'),
            "jrPlatform": "ACTIVITY",
            "ua": self.useragent.replace(" ", "+"),
            "cookie": "",
            "actId": self.actId,
            "answerId": sal_id,
        }
        resp = self.session.post(url=url, data=data)
        result = resp.json()
        try:
            reward_name = f"答题_{self.now_time}_{result['data']['sbl_reward_name']}"
            self.recordPrize(reward_name)
            print(json.dumps(result, indent=4, ensure_ascii=False))
        except Exception as e:
            print(e)
            print(resp.json())

    def userActInfo(self, debug=False):
        url = 'https://edu.10155.com/wxx-api/Api/Stdthd/userActInfo'
        data = {
            "p": "",
            "chc": self.config.get('chc'),
            "jrPlatform": "ACTIVITY",
            "ua": self.useragent.replace(" ", "+"),
            "cookie": "",
            "actId": self.actId
        }
        resp = self.session.post(url=url, data=data)
        result = resp.json()
        print(resp.headers.get('Set-Cookie', None))
        if result['message'].find('登录') > -1:
            print(result['message'])
            self.isLogin = False
        try:
            self.prizeList = result['data']['reward'][-10:]
            if not debug:
                result['data']['reward'] = result['data']['reward'][-1:]
        except Exception as e:
            print(str(e))
        print(json.dumps(result, indent=4, ensure_ascii=False))
        try:
            self.sal_id = result['data']['answer']['sal_id']
            # self.sal_answer_days = int(
            #     result['data']['answer'].get('sal_answer_days', 0)
            # )
            if not result['data']['round']:
                self.srl_success_days = 0
            else:
                self.srl_success_days = int(result['data']['round']['srl_success_days'])
            self.sal_get_bonus = int(
                result['data']['answer'].get('sal_get_bonus', 0)
            )
            self.sal_is_bonus = int(
                result['data']['answer'].get('sal_is_bonus', 0)
            )
            self.sal_answer_status = int(
                result['data']['answer'].get('sal_answer_status', 0)
            )
            self.sal_answer_chances = int(
                result['data']['answer'].get('sal_answer_chances', 0)
            )
            self.sal_wrong_num = int(
                result['data']['answer'].get('sal_wrong_num', 0)
            )
        except Exception as e:
            print(str(e))
            self.sal_id = ""
            # self.sal_answer_days = 0
            self.srl_success_days = 0
            self.sal_get_bonus = 0
            self.sal_is_bonus = 0
            self.sal_answer_status = 0
            self.sal_answer_chances = 0
            self.sal_wrong_num = 0

    def actInfo(self):
        url = 'https://edu.10155.com/wxx-api/Api/Stdthd/actInfo'
        data = {
            "p": "",
            "chc": self.config.get('chc'),
            "jrPlatform": "ACTIVITY",
            "ua": self.useragent.replace(" ", "+"),
            "cookie": "",
            "actId": self.actId
        }
        resp = self.session.post(url=url, data=data)
        result = resp.json()
        # print(json.dumps(result, indent=4, ensure_ascii=False))
        return result['data']['today']

    def answer(self, item, answerId):
        url = 'https://edu.10155.com/wxx-api/Api/Stdthd/answer'
        data = {
            "p": "",
            "chc": self.config.get('chc'),
            "jrPlatform": "ACTIVITY",
            "ua": self.useragent.replace(" ", "+"),
            "cookie": "",
            "actId": self.actId,
            "questionId": item['sq_id'],
            "answerId": answerId,
        }
        resp = self.session.post(url=url, data=data)
        result = resp.json()
        print(json.dumps(result, indent=4, ensure_ascii=False))
        return int(result['data']['status'])

    def addRaffleChance(self, orderId, sal_id):
        url = 'https://edu.10155.com/wxx-api/Api/Stdthd/addRaffleChance'
        data = {
            "p": "",
            "chc": self.config.get('chc'),
            "jrPlatform": "ACTIVITY",
            "ua": self.useragent.replace(" ", "+"),
            "phone": self.mobile,
            "cookie": "",
            "answerId": sal_id,
            "orderId": orderId
        }
        resp = self.session.post(url=url, data=data)
        result = resp.json()
        print(json.dumps(result, indent=4, ensure_ascii=False))

    def addAnswerChance(self, orderId, sal_id):
        url = 'https://edu.10155.com/wxx-api/Api/Stdthd/addAnswerChance'
        data = {
            "p": "",
            "chc": self.config.get('chc'),
            "jrPlatform": "ACTIVITY",
            "ua": self.useragent.replace(" ", "+"),
            "phone": self.mobile,
            "cookie": "",
            "answerId": sal_id,
            "orderId": orderId
        }
        resp = self.session.post(url=url, data=data)
        result = resp.json()
        print(json.dumps(result, indent=4, ensure_ascii=False))

    def handlePrize(self):
        for item in self.prizeList:
            if int(item['sbl_reward_status']) or int(item['sbl_reward_id']) in [16, 17, 19]:
                continue
            else:
                print(item)
                self.getReward(item)
                self.flushTime(1)

    def run(self):
        self.userActInfo()
        if not self.isLogin or self.config['timestamp'][:8] != self.now_date.replace('-', ''):
            self.isLogin = True
            self.openPlatLineNew(
                'https://edu.10155.com/wact/stdt5.html?jrPlatform=SHOUTING&chc=CC1XJwYxUCkHYgx1V2MGO1NjUitXOg&vid=-1'
            )
            self.shoutingTicketLogin(self.chc)
            self.userActInfo()
        if not self.isLogin:
            print('登录失败')
            return
        if self.sal_is_bonus == self.sal_get_bonus and self.sal_get_bonus:
            # "sal_is_bonus": "2",
            # "sal_get_bonus": "1"
            # "sal_is_bonus": "1",  # 抽奖机会次数
            # "sal_get_bonus": "0"  # 已抽奖次数
            print('抽奖机会已用完')
            return
        item = self.actInfo()
        length = len(item['sq_options'])

        if not self.sal_is_bonus and not self.sal_answer_status:
            for answerId in range(length):
                if not self.sal_answer_status:
                    if self.sal_id and self.sal_answer_chances <= self.sal_wrong_num:
                        self.flushTime(randint(10, 15))
                        options = {
                            'arguments1': '',
                            'arguments2': '',
                            'codeId': 945905993,
                            'remark': '教育频道答题抽奖活动',
                            'ecs_token': self.session.cookies.get('ecs_token')
                        }
                        orderId = self.toutiao.reward(options)
                        self.addAnswerChance(orderId, self.sal_id)
                    if self.answer(item, answerId) == 1:
                        self.userActInfo()
                    else:
                        self.userActInfo()
                        continue
                    if self.sal_id and self.srl_success_days >= 2:
                        self.flushTime(randint(10, 15))
                        options = {
                            'arguments1': '',
                            'arguments2': '',
                            'codeId': 945905993,
                            'remark': '教育频道答题抽奖活动',
                            'ecs_token': self.session.cookies.get('ecs_token')
                        }
                        orderId = self.toutiao.reward(options)
                        self.addRaffleChance(orderId, self.sal_id)
                    break
        self.userActInfo()
        if self.srl_success_days >= 2:
            self.raffle(self.sal_id)
        self.handlePrize()


if __name__ == '__main__':
    pass
