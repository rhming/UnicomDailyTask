# -*- coding: utf8 -*-
import json
import time
from activity.womail.womail import WoMail


class Puzzle2(WoMail):

    def __init__(self, mobile, openId):
        super(Puzzle2, self).__init__(mobile, openId)
        self.session.headers.update({
            'Referer': 'https://nyan.mail.wo.cn/cn/puzzle2/wap/index.html',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; MI 8 SE Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2797 MMWEBSDK/20210501 Mobile Safari/537.36 MMWEBID/107 MicroMessenger/8.0.6.1900(0x28000635) Process/toolsmp WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64',
            'X-Requested-With': 'com.tencent.mm'  # XMLHttpRequest
        })

    def login(self):
        url = f'https://nyan.mail.wo.cn/cn/puzzle2/index/index?mobile={self.mobile}&userName=&openId={self.openId}'
        self.session.get(url=url)
        print(self.session.cookies.get_dict())

    def index(self):
        url = 'https://nyan.mail.wo.cn/cn/puzzle2/wap/index.html'
        self.session.get(url=url)

    def clear(self):
        url = 'https://nyan.mail.wo.cn/cn/puzzle2/user/clear.do'
        self.session.get(url=url)

    def userInfo(self):
        url = f'https://nyan.mail.wo.cn/cn/puzzle2/index/userinfo.do?time={self.timestamp}'
        resp = self.session.post(url=url)
        try:
            data = resp.json()
            print(json.dumps(data, indent=4, ensure_ascii=False))
            return data['result']['usedChance'], data['result']['puzzle']
        except:
            print(resp.text)
            return 1, 0

    def prizeDetail(self):
        url = f'https://nyan.mail.wo.cn/cn/puzzle2/user/prizes.do?time={self.timestamp}'
        resp = self.session.post(url=url)
        data = resp.json()
        if len(data['result']) > 3:
            data['result'] = data['result'][:3]
        print(json.dumps(data, indent=4, ensure_ascii=False))

    def doTask(self, task_name):
        url = f'https://nyan.mail.wo.cn/cn/puzzle2/user/doTask.do'
        params = {
            'taskName': task_name
        }
        resp = self.session.get(url=url, params=params)
        print(resp.text)

    def overTask(self):
        url = f'https://nyan.mail.wo.cn/cn/puzzle2/user/overtask.do?time={self.timestamp}'
        resp = self.session.get(url=url)
        data = resp.json()
        print(json.dumps(data, indent=4, ensure_ascii=False))
        result = [item['taskName'] for item in data['result']]
        return result

    def draw(self):
        url = 'https://nyan.mail.wo.cn/cn/puzzle2/draw/draw'
        resp = self.session.get(url=url)
        print(resp.json())

    def run(self):
        try:
            self.login()
            self.index()
            _, puzzle = self.userInfo()
            overTaskList = self.overTask()
            for taskName in ['checkin', 'loginmail', 'viewclub']:
                if taskName in overTaskList:
                    continue
                self.doTask(taskName)
                time.sleep(3)
            _, puzzle = self.userInfo()
            self.clear()
            if puzzle == 6:
                self.draw()
                self.prizeDetail()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    pass
