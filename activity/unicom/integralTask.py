# -*- coding: utf8 -*-
from random import randint
from utils.toutiao_reward import TouTiao
from utils.unicomLogin import UnicomClient


class IntegralTask(UnicomClient):

    def __init__(self, mobile, password):
        super(IntegralTask, self).__init__(mobile, password)
        self.toutiao = TouTiao(mobile)

    def executeIntegralTask(self, acId, taskId, codeId, channelName, remark):
        acId = acId  # "AC20200728150217"
        taskId = taskId  # "96945964804e42299634340cd2650451"
        if self.taskcallbackquery(acId, taskId):
            options = {
                'arguments1': acId,
                'arguments2': taskId,
                'codeId': codeId,  # 945535736,
                'channelName': channelName,
                'remark': remark,  # '游戏频道看视频得积分',
                'ecs_token': self.session.cookies.get('ecs_token')
            }
            self.flushTime(randint(10, 15))
            orderId = self.toutiao.reward(options)
            self.taskcallbackdotasks(acId, taskId, orderId, remark)
            return True
        else:
            return False

    def run(self):
        self.onLine()
        items = [
            {
                "acId": "AC20200624091508",
                "taskId": "734225b6ec9946cca3bcdc6a6e14fc1f",
                "codeId": "945535704",
                "channelName": "android-签到看视频翻倍得积分-激励视频",
                "remark": "签到看视频得积分"
            },
            {
                'acId': 'AC20200716103629',
                'taskId': 'a42de1cf969945eb87b529c4763ab6e5',
                'codeId': "945535637",
                'channelName': 'new-android-签到小游戏霸王餐积分翻倍-激励视频',
                'remark': '签到小游戏翻倍得积分'
            },
            {
                "acId": "AC20200716103629",
                "taskId": "fc32b68892de4299b6ccfb2de72e1ab8",
                "codeId": "946169925",
                "channelName": "android-签到小游戏幸运转盘-激励视频",
                "remark": "签到小游戏翻倍得积分",
            },
            {
                'acId': 'AC20200611152252',
                'taskId': '10131519d6e14f1b97b13cb627d956e5',
                'codeId': '945535633',
                'channelName': 'android-签到小游戏乐开盲盒-激励视频',
                'remark': '签到小游戏翻倍得积分',
            },
            {
                'acId': 'AC20200611152252',
                'taskId': 'f34bec559ce248a5bbba0a59a7969e41',
                'codeId': '945689604',
                'channelName': 'android-签到小游戏摇摇乐不倒翁-激励视频',
                'remark': '签到小游戏翻倍得积分',
            },
            {
                'acId': 'AC20200716103629',
                'taskId': '23cdde55584547369d70fa61093956cc',
                'codeId': '945719787',
                'channelName': 'android-签到小游戏开心抓大奖-激励视频',
                'remark': '签到页小游戏抓娃娃积分翻倍',
            },
            {
                'acId': 'AC20200716103629',
                'taskId': 'cc71671332524a09ab0f444f4562c752',
                'codeId': '945597731',
                'channelName': 'android-签到小游戏买什么都省幸运刮刮乐积分翻倍-激励视频',
                'remark': '签到小游戏翻倍得积分',
            },
            {
                'acId': 'AC20200716103629',
                'taskId': '79b0275d6a5742ce96af76a663cde0ab',
                'codeId': '945597731',
                'channelName': 'android-签到小游戏买什么都省幸运刮刮乐积分翻倍-激励视频',
                'remark': '签到小游戏翻倍得积分',
            },
            {
                'acId': 'AC20200716103629',
                'taskId': '810d279fa7ec478289315e61e8e4322f',
                'codeId': '946179170',
                'channelName': 'android-签到小游戏套牛积分翻倍-激励视频',
                'remark': '签到页小游戏翻倍得积分',
            },
            {
                'acId': 'AC20200716103629',
                'taskId': 'e9571adf96004762af4e375263f5630c',
                'codeId': '945793197',
                'channelName': 'android-签到积分翻倍-激励视频',
                'remark': '签到页小游戏翻倍得积分',
            },
            {
                'acId': 'AC20200716103629',
                'taskId': 'ba6b14db2ff4438297449fa827ff449e',
                'codeId': '945793197',
                'channelName': 'android-签到积分翻倍-激励视频',
                'remark': '签到页小游戏翻倍得积分',
            },
            {
                'acId': 'AC20200716103629',
                'taskId': '7c6b859434c2403fb34607c349994828',
                'codeId': '946179170',
                'channelName': 'android-签到小游戏套牛积分翻倍-激励视频',
                'remark': '签到页小游戏翻倍得积分',
            },
        ]
        length = len(items)
        for _, item in enumerate(items, 1):
            flag = self.executeIntegralTask(**item)
            if _ != length and flag:
                self.flushTime(randint(5, 10))


if __name__ == '__main__':
    pass
