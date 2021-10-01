# -*- coding: utf8 -*-
from random import randint
from utils.toutiao_reward import TouTiao
from utils.unicomLogin import UnicomClient


class IntegralTask(UnicomClient):

    def __init__(self, mobile, password):
        super(IntegralTask, self).__init__(mobile, password)
        self.toutiao = TouTiao(mobile)

    def executeIntegralTask(self, acId, taskId, codeId, remark):
        acId = acId  # "AC20200728150217"
        taskId = taskId  # "96945964804e42299634340cd2650451"
        if self.taskcallbackquery(acId, taskId):
            options = {
                'arguments1': acId,
                'arguments2': taskId,
                'codeId': codeId,  # 945535736,
                'remark': remark,  # '游戏频道看视频得积分',
                'ecs_token': self.session.cookies.get('ecs_token')
            }
            self.flushTime(randint(15, 25))
            orderId = self.toutiao.reward(options)
            self.taskcallbackdotasks(acId, taskId, orderId, remark)

    def run(self):
        # self.onLine()
        if not self.checklogin():
            self.onLine()
        items = [
            {
                "acId": "AC20200624091508",
                "taskId": "734225b6ec9946cca3bcdc6a6e14fc1f",
                "codeId": "945535704",
                "remark": "签到看视频得积分"
            },
        ]
        length = len(items)
        for _, item in enumerate(items, 1):
            self.executeIntegralTask(**item)
            if _ != length:
                self.flushTime(randint(10, 15))


if __name__ == '__main__':
    pass
