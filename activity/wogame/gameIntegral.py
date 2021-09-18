# -*- coding: utf8 -*-
# import json
from random import randint
from utils import jsonencode as json
from utils.toutiao_reward import TouTiao
from activity.wogame.wogame import WoGame


class GameIntegral(WoGame):
    """
        联通手厅游戏积分活动
    """

    def __init__(self, mobile, password):
        super(GameIntegral, self).__init__(mobile, password)
        self.toutiao = TouTiao(mobile)

    def queryTaskCenter(self):
        url = 'https://m.client.10010.com/producGameTaskCenter'
        data = {
            'methodType': 'queryTaskCenter',
            'clientVersion': self.clientVersion,
            'deviceType': 'Android',
        }
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        data = resp.json()
        print(json.dumps(data, indent=4, ensure_ascii=False))
        self.gameTaskDetail = {
            d['task_title']: [
                d['task_reward'], d["qq_mark"], d['progress'],
                d['task'], d["url"], d["reachState"]
            ]
            for d in data['data']
        }
        print(self.gameTaskDetail)
        return data['data']

    def queryIntegral(self, item):
        url = 'https://m.client.10010.com/producGameTaskCenter'
        data = {
            'methodType': 'queryIntegral',
            'taskCenterId': item['id'],
            'videoIntegral': item['task_reward'],
            'isVideo': 'Y',
            'clientVersion': self.clientVersion,
            'deviceType': 'Android',
        }
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        data = resp.json()
        print(json.dumps(data, indent=4, ensure_ascii=False))

    def getReward(self, item):
        url = 'https://m.client.10010.com/producGameTaskCenter'
        data = {
            'methodType': 'taskGetReward',
            'taskCenterId': item['id'],
            'clientVersion': self.clientVersion,
            'deviceType': 'Android',
        }
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        data = resp.json()
        print(json.dumps(data, indent=4, ensure_ascii=False))

    def playGame(self, item):
        self.firsttime = None
        self.reporttime = []
        print(json.dumps(item, indent=4, ensure_ascii=False))

        verify_data = self.gameVerify()
        if verify_data['extInfo'] != self.session.cookies.get('jwt'):
            self.onLine()

        if int(item['task']) != int(item['progress']):
            if item['progress'] == '0':
                self.clickRecord(item['game_id'])
            minute = int(item['task'])
            print(f'总计{minute}分钟')
            game_url = item['url'].strip()
            if game_url.find('wostore') > -1:
                self.qucikLogin(game_url)
                for _ in range(minute + 1):
                    print(f'需报告{minute + 1}次,第{_ + 1}次报告中...')
                    self.flushTime(60)
                    self.reportedGame(game_url)
                    self.queryTaskCenter()
                self.flushTime(10)
                self.qucikLogin(game_url)
                self.flushTime(10)
                self.queryTaskCenter()
            else:
                for _ in range(1, minute + 1):
                    print(f'需报告{minute}次,第{_}次报告中...')
                    self.judgeTime(item['resource_id'], minute, _)
                    self.flushTime(60)
                    self.queryTaskCenter()
                self.flushTime(10)
        if int(self.gameTaskDetail[item['task_title']][2]) == int(self.gameTaskDetail[item['task_title']][3]):
            self.getReward(item)

    def watchVideo(self, item):
        acId = "AC20200728150217"
        taskId = "96945964804e42299634340cd2650451"
        if self.taskcallbackquery(acId, taskId):
            options = {
                'arguments1': acId,
                'arguments2': taskId,
                'codeId': 945535736,
                'remark': '游戏频道看视频得积分',
                'ecs_token': self.session.cookies.get('ecs_token')
            }
            self.flushTime(randint(30, 35))
            orderId = self.toutiao.reward(options)
            self.taskcallbackdotasks(acId, taskId, orderId, options['remark'])
            self.flushTime(randint(5, 10))
        self.queryIntegral(item)

    def drawTask(self, item):
        pass

    def run(self):
        if self.last_login_time.find(self.now_date) == -1:
            self.onLine()
        gameTaskList = self.queryTaskCenter()
        # return
        for item in gameTaskList:
            if int(item['reachState']) == 2 or item['task_title'] == '完成今日任务':
                continue
            if item['game_id'] and item['url']:
                self.playGame(item)
                return
            if item['task_title'] == '看视频得积分':
                print('看视频任务')
                self.watchVideo(item)
                self.queryTaskCenter()
                return
            if item['task_title'] == '抽奖任务':
                print('抽奖任务')
                self.drawTask(item)
                return
            if item['task_title'] == '完成今日任务':
                print('完成今日任务')
                return


if __name__ == '__main__':
    pass
