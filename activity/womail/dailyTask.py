# -*- coding: utf8 -*-
import json
from activity.womail.womail import WoMail


class DailySign(WoMail):

    def __init__(self, mobile, openId):
        super(DailySign, self).__init__(mobile, openId)
        self.session.headers.update({
            # 'Origin': 'https://nyan.mail.wo.cn',
            'Referer': 'https://nyan.mail.wo.cn/cn/sign/wap/index.html',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; MI 8 SE Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2797 MMWEBSDK/20210501 Mobile Safari/537.36 MMWEBID/107 MicroMessenger/8.0.6.1900(0x28000635) Process/toolsmp WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64',
            'X-Requested-With': 'com.tencent.mm'  # XMLHttpRequest
        })
        self.message = ''

    def login(self):
        url = f'https://nyan.mail.wo.cn/cn/sign/index/index?mobile={self.mobile}&userName=&openId={self.openId}'
        self.session.get(url=url)
        print(self.session.cookies.get_dict())

    def index(self):
        url = 'https://nyan.mail.wo.cn/cn/sign/wap/index.html'
        self.session.get(url=url)

    def userInfo(self):
        url = f'https://nyan.mail.wo.cn/cn/sign/index/userinfo.do?rand={self.randomNum}'
        resp = self.session.post(url=url)
        data = resp.json()
        try:
            print(json.dumps(data, indent=4, ensure_ascii=False))
            return str(data['result']['lastDay']), str(data['result']['keepSign'])
        except:
            print(resp.text)

    def isLogin(self):
        url = f'https://nyan.mail.wo.cn/cn/sign/user/isLoginMail.do?rand={self.randomNum}'
        resp = self.session.post(url=url)
        print(resp.text)

    def check(self):
        url = f'https://nyan.mail.wo.cn/cn/sign/user/checkin.do?rand={self.randomNum}'
        resp = self.session.post(url=url)
        print(resp.text)

    def prizeDetail(self):
        url = f'https://nyan.mail.wo.cn/cn/sign/user/prizes.do?rand={self.randomNum}'
        resp = self.session.post(url=url)
        data = resp.json()
        if len(data['result']) > 3:
            data['result'] = data['result'][:3]
        print(json.dumps(data, indent=4, ensure_ascii=False))

    def doTask(self, task_name):
        url = f'https://nyan.mail.wo.cn/cn/sign/user/doTask.do?rand={self.randomNum}'
        data = {
            'taskName': task_name
        }
        resp = self.session.post(url=url, data=data)
        print(resp.text)

    def overTask(self):
        url = f'https://nyan.mail.wo.cn/cn/sign/user/overtask.do?rand={self.randomNum}'
        data = {
            'taskLevel': '2'
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(json.dumps(data, indent=4, ensure_ascii=False))
        result = [item['taskName'] for item in data['result']]

        # data = {
        #     'taskLevel': '1'
        # }
        return result

    def run(self):
        try:
            self.login()
            self.index()
            result = self.overTask()
            for task_name in ["loginmail", "clubactivity", "club"]:  # , "download"
                if task_name in result:
                    continue
                self.doTask(task_name)
                self.flushTime(1)
            else:
                print("积分签到任务已完成")
            lastDay, keepSign = self.userInfo()
            if keepSign == '21':
                print('跳过21天之后的打卡')
                self.message = '每日签到: 跳过21天之后的打卡'
                self.recordLog(self.message)
                return
            else:
                if self.now_date.replace('-', '') == lastDay:
                    print("今日已打卡")
                    return
                else:
                    self.check()
                    self.prizeDetail()
                lastDay, _ = self.userInfo()
                if self.now_date.replace('-', '') == lastDay:
                    self.message = '每日签到: 已签到'
                else:
                    self.message = '每日签到: 未签到'
                self.recordLog(self.message)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    pass
