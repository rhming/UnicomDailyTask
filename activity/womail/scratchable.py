# -*- coding: utf8 -*-
import time
import json
from activity.womail.womail import WoMail


class Scratchable(WoMail):

    def __init__(self, mobile, openId):
        super(Scratchable, self).__init__(mobile, openId)
        self.session.headers.update({
            # 'Origin': 'https://club.mail.wo.cn',
            'Referer': 'https://club.mail.wo.cn/ActivityWeb/scratchable/wap/template/index.html?activityId=387&resourceId=wo-wx',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; MI 8 SE Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2797 MMWEBSDK/20210501 Mobile Safari/537.36 MMWEBID/107 MicroMessenger/8.0.6.1900(0x28000635) Process/toolsmp WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64',
            'X-Requested-With': 'com.tencent.mm'  # XMLHttpRequest
        })

    def login(self):
        url = f'https://club.mail.wo.cn/ActivityWeb/activity-web/index?activityId=387&typeIdentification=scratchable&resourceId=wo-wx&mobile={self.mobile}&userName=&openId={self.openId}'
        self.session.get(url=url)
        print(self.session.cookies.get_dict())

    def index(self):
        url = 'https://club.mail.wo.cn/ActivityWeb/activity-web/index?activityId=387&typeIdentification=scratchable&resourceId=wo-wx'
        self.session.get(url=url)

    def activityInfo(self):
        url = 'https://club.mail.wo.cn/ActivityWeb/activity-detail/activity-info?activityId=387'
        self.session.get(url=url)

    def activityPrize(self):
        url = 'https://club.mail.wo.cn/ActivityWeb/activity-detail/activity-prize?activityId=387'
        self.session.get(url=url)

    def activityPrizeAsc(self):
        url = 'https://club.mail.wo.cn/ActivityWeb/activity-detail/activity-prize-asc?activityId=387'
        self.session.get(url=url)

    def surplusTimes(self):
        url = 'https://club.mail.wo.cn/ActivityWeb/activity-detail/surplus-times'
        data = {
            "participateDate": time.strftime("%Y-%m-%d", time.localtime(self.timestamp / 1000)),
            "activityId": "387"
        }
        resp = self.session.post(url=url, json=data)
        try:
            data = resp.json()
            print(data)
            return data.get('data', 0)
        except:
            print(resp.text)
            return 0

    def getPrizeList(self):
        url = 'https://club.mail.wo.cn/ActivityWeb/activity-function/activity-record'
        data = {
            "activityId": "387",
            "awarded": True
        }
        resp = self.session.post(url=url, json=data)
        try:
            result = resp.json()
            if len(result['data']) > 3:
                result['data'] = result['data'][:3]
            print(json.dumps(result, indent=4, ensure_ascii=False))
        except:
            print(resp.text)

    def getPrizeIndex(self):
        url = 'https://club.mail.wo.cn/ActivityWeb/activity-function/get-prize-index'
        data = {
            "participateDate": time.strftime("%Y-%m-%d", time.localtime(self.timestamp / 1000)),
            "activityId": "387"
        }
        resp = self.session.post(url=url, json=data)
        try:
            print(resp.json())
        except:
            print(resp.text)
        data = resp.json()['data']
        if data['prizeType'] == 'THANKS_PARTICIPATE':
            return
        self.sendPrize(data['prizeId'], data['recordNo'], data['prizeType'])

    def sendPrize(self, prizeId, recordNo, prizeType, address=""):
        url = 'https://club.mail.wo.cn/ActivityWeb/activity-function/send-prize'
        data = {
            "prizeId": prizeId,
            "recordNo": recordNo,
            "address": address,
            "prizeType": prizeType
        }
        resp = self.session.post(url=url, json=data)
        try:
            print(resp.json())
        except:
            print(resp.text)

    def activityRecord(self):
        url = 'https://club.mail.wo.cn/ActivityWeb/activity-function/activity-record'
        data = {
            "activityId": "387",
            "awarded": True
        }
        resp = self.session.post(url=url, json=data)
        try:
            result = resp.json()
            if len(result['data']) > 3:
                result['data'] = result['data'][:3]
            print(json.dumps(result, indent=4, ensure_ascii=False))
        except:
            print(resp.text)

    def run(self):
        try:
            self.login()
            self.index()
            # self.activityInfo()
            # self.activityPrize()
            data = self.surplusTimes()
            if data:
                # for i in range(1, data + 1):
                try:
                    print(f'--->第{2 - data + 1}次抽奖')
                    self.getPrizeIndex()
                except Exception as e:
                    print(e)
            self.activityRecord()
            self.getPrizeList()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    pass
