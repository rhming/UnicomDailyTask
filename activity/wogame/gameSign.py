# -*- coding: utf8 -*-
import time
import json
from activity.wogame.wogame import WoGame


class GameSign(WoGame):
    """
        游戏中心日常签到
    """

    def __init__(self, mobile, password):
        super(GameSign, self).__init__(mobile, password)

    def index(self):
        url = 'https://img.client.10010.com/gametask/index.html?yw_code=&desmobile=%s&version=%s' % (
            self.mobile,
            self.version
        )
        self.session.get(url=url)

    def signHistory(self):
        url = 'https://m.client.10010.com/producGame_signin'
        data = {
            'methodType': 'signin_history',
            'clientVersion': self.clientVersion,
            'deviceType': 'Android'
        }
        resp = self.session.post(url=url, data=data, allow_redirects=False)
        resp.encoding = 'utf8'
        try:
            data = resp.json()
            data['signin_history'] = json.loads(data['signin_history'])
        except:
            print(resp.text)
            return
        # print(json.dumps(data, indent=4, ensure_ascii=False))
        return data['currentIntegralState']

    def signIn(self):
        url = 'https://m.client.10010.com/producGame_signin'
        data = {
            'methodType': 'signin',
            'sign_flag': '1',
            'clientVersion': self.clientVersion,
            'deviceType': 'Android'
        }
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        data = resp.json()
        print(json.dumps(data, indent=4, ensure_ascii=False))

    def run(self):
        date = int(time.strftime(
            "%Y%m%d",
            time.localtime(self.timestamp / 1000)
        ))
        if date <= 20210821:
            self.index()
            if self.signHistory() == '1':
                print("今日已签到")
            else:
                self.signIn()
        else:
            print("活动已下线")


if __name__ == "__main__":
    pass
