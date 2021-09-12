# -*- coding: utf8 -*-
# import json
from random import randint
from utils import jsonencode as json
from activity.wolearn.wolearn import WoLearn


class WzsbzAct(WoLearn):

    def __init__(self, mobile, password):
        super(WzsbzAct, self).__init__(mobile, password)
        self.chc = "VVBaClZJBQhSDFcpUnFbbgcvAQMDFQIoVmNfZg"
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

    def getReward(self, item):
        url = 'https://edu.10155.com/wxx-api/Api/WzsbzAct/getReward'
        data = {
            "p": "",
            "chc": self.config.get('chc'),
            "jrPlatform": "ACTIVITY",
            "ua": self.useragent.replace(" ", "+"),
            "cookie": "",
            "bonusId": item['wbl_id'],
            "account": self.mobile
        }
        if item['wbl_reward_log']:
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

    def raffle(self):
        url = 'https://edu.10155.com/wxx-api/Api/WzsbzAct/raffle'
        data = {
            "p": "",
            "chc": self.config.get('chc'),
            "jrPlatform": "ACTIVITY",
            "ua": self.useragent.replace(" ", "+"),
            "cookie": "",
            "jackpot": "2"  # 1 / 2 (第一个 第二个 宝箱)
        }
        resp = self.session.post(url=url, data=data)
        result = resp.json()
        try:
            reward_name = f"挖宝_{self.now_time}_{result['data']['wbl_reward_name']}"
            self.recordPrize(reward_name)
            print(json.dumps(result, indent=4, ensure_ascii=False))
        except Exception as e:
            print(e)
            print(resp.text)

    def userActInfo(self, debug=False):
        url = 'https://edu.10155.com/wxx-api/Api/WzsbzAct/userActInfo'
        data = {
            "p": "",
            "chc": self.config.get('chc'),
            "jrPlatform": "ACTIVITY",
            "ua": self.useragent.replace(" ", "+"),
            "cookie": ""
        }
        resp = self.session.post(url=url, data=data)
        result = resp.json()
        print(resp.headers.get('Set-Cookie', None))
        if result['message'].find('登录') > -1:
            print(result['message'])
            self.isLogin = False
            return 0, 1, 5
        try:
            self.prizeList = result['data']['reward'][-10:]
            if not debug:
                result['data']['reward'] = result['data']['reward'][-1:]
        except Exception as e:
            print(str(e))
        print(json.dumps(result, indent=4, ensure_ascii=False))
        lottery_times = result['data']['lottery_times']
        lottery_chance = result['data']['lottery_chance']
        possible_chances = result['data']['possible_chances']
        # lottery_data = result['data']['lottery_data']
        # if lottery_data:
        #     jackpot = lottery_data.get('jackpot', 2)
        # else:
        #     jackpot = 2
        return (
            int(lottery_times) if lottery_times else 0,
            int(lottery_chance) if lottery_chance else 1,
            int(possible_chances) if possible_chances else 5,
            # int(jackpot)
        )

    def addRaffleChance(self, orderId, tip):
        url = 'https://edu.10155.com/wxx-api/Api/WzsbzAct/addRaffleChance'
        data = {
            "p": "",
            "chc": self.config.get('chc'),
            "jrPlatform": "ACTIVITY",
            "ua": self.useragent.replace(" ", "+"),
            "phone": self.mobile,
            "cookie": "",
            "orderId": orderId
        }
        # if tip:
        #     data['type'] = tip
        resp = self.session.post(url=url, data=data)
        result = resp.json()
        print(json.dumps(result, indent=4, ensure_ascii=False))

    def handlePrize(self):
        for item in self.prizeList:
            if int(item['wbl_reward_status']) or int(item['wbl_reward_id']) in [103, 104, 105, 106, 209, 210, 211, 212]:
                continue
            else:
                print(item)
                self.getReward(item)
                self.flushTime(3)

    def run(self):
        info = lottery_times, lottery_chance, possible_chances = self.userActInfo()
        if not self.isLogin or self.config['timestamp'][:8] != self.now_date.replace('-', ''):
            self.isLogin = True
            self.openPlatLineNew(
                'https://edu.10155.com/wact/wabao.html?jrPlatform=SHOUTING&chc=VVBaClZJBQhSDFcpUnFbbgcvAQMDFQIoVmNfZg&vid=-1'
            )
            self.shoutingTicketLogin(self.chc)
            info = lottery_times, lottery_chance, possible_chances = self.userActInfo()
        print(info)
        if not self.isLogin:
            print('登录失败')
            return
        if possible_chances == lottery_times:
            print('抽奖次数用完')
            return
        if lottery_times == 0 or lottery_times == lottery_chance:
            self.flushTime(randint(10, 15))
            tip = None
            options = {
                'arguments1': '',
                'arguments2': '',
                'codeId': 945994875,
                'remark': '教育频道热点活动',
                'ecs_token': self.session.cookies.get('ecs_token')
            }
            orderId = self.toutiao.reward(options)
            # if lottery_times == 0:
            #     tip = 'goodLuck'  # 额外两次 触发
            self.addRaffleChance(orderId, tip)
        self.raffle()
        self.userActInfo()
        self.handlePrize()


if __name__ == '__main__':
    pass
