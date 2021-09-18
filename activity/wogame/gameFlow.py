# -*- coding: utf8 -*-
# import json
import time
from activity.wogame.wogame import WoGame
from utils import jsonencode as json


class GameFlow(WoGame):
    """
        联通手厅游戏抽流量活动
    """

    def __init__(self, mobile, password):
        super(GameFlow, self).__init__(mobile, password)

    def popularGames(self):
        url = 'https://m.client.10010.com/producGameApp'
        data = {
            "deviceType": "Android",
            "methodType": "popularGames",
            "clientVersion": self.clientVersion,
            "isHtml": "1"  # h5
        }
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        data = resp.json()
        self.gameTaskDetail = {
            d['name']: [
                d['flow'], d["qqMark"], d["minute"],
                d["currentMinute"], d["url"], d["state"]
            ]
            for d in data['popularList']
        }
        print(json.dumps(self.gameTaskDetail, indent=4, ensure_ascii=False))
        return data['popularList']

    def flowGet(self, gameId, retry=1):
        """
            完成任务后领取流量  (需要满足任务记录时间)
        """

        url = 'https://m.client.10010.com/producGameApp'
        data = {
            "methodType": "flowGet",
            "deviceType": "Android",
            "clientVersion": self.clientVersion,
            "gameId": gameId,
            "isHtml": "1"  # h5
        }
        resp = self.session.post(url=url, data=data, allow_redirects=False)
        resp.encoding = 'utf8'
        print(resp.text)
        if resp.status_code != 200 and retry > 0:
            self.flushTime(5)
            self.flowGet(gameId, retry - 1)

    def run(self):
        if self.last_login_time.find(self.now_date) == -1:
            self.onLine()
        popularList = self.popularGames()  # type: list

        for item in popularList:
            if item['state'] == '2' or int(item['flow']) < 100 or not int(item['minute']):
                continue
            self.firsttime = None
            self.reporttime = []
            print(json.dumps(item, indent=4, ensure_ascii=False))

            verify_data = self.gameVerify()
            if verify_data['extInfo'] != self.session.cookies.get('jwt'):
                self.onLine()
            if int(item['currentMinute']) != int(item['minute']):
                if item['state'] == '0':
                    self.clickrecord(item['id'])
                    # self.iosTaskRecord(item['id'])
                minute = int(item['minute'])
                print(f'总计{minute}分钟')
                game_url = item['url'].strip()
                if game_url.find('wostore') > -1:
                    self.qucikLogin(game_url)
                    for _ in range(minute + 1):
                        print(f'需报告{minute + 1}次,第{_ + 1}次报告中...')
                        self.flushTime(60)
                        self.reportedGame(game_url)
                        self.popularGames()
                    self.flushTime(10)
                    self.qucikLogin(game_url)
                    self.flushTime(10)
                    self.popularGames()
                else:
                    for _ in range(1, minute + 1):
                        print(f'需报告{minute}次,第{_}次报告中...')
                        self.judgeTime(item['resourceId'], minute, _)
                        self.flushTime(60)
                        self.popularGames()
                    self.flushTime(10)
            if int(self.gameTaskDetail[item['name']][2]) == int(self.gameTaskDetail[item['name']][3]):
                self.flowGet(item['id'])
            break


if __name__ == '__main__':
    pass
