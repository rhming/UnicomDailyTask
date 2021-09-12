# -*- coding: utf8 -*-
from random import randint
from activity.woread.woread import WoRead


class FlowDraw(WoRead):

    def __init__(self, mobile, _=None):
        super(FlowDraw, self).__init__(mobile)
        self.session.cookies.update({
            'Referer': 'https://st.woread.com.cn/touchextenernal/read/index.action?channelid=18000827&type=1'
        })

    def index(self):
        url = f'https://st.woread.com.cn/touchextenernal/read/index.action?channelid=18000827&type=1'
        resp = self.session.get(url=url)
        cookies = resp.cookies.get_dict()
        if cookies.get('JSESSIONID', False):
            self.saveCookie(f'{self.mobile}WoRead', self.session.cookies.get_dict())

    def getGrowScore(self):
        url = 'http://st.woread.com.cn/touchextenernal/read/getGrowScore.action'
        resp = self.session.post(url=url)
        print(self.mobile + ' ' + resp.text)

    def ajaxUpdatePersonReadtime(self):
        url = 'http://st.woread.com.cn/touchextenernal/contentread/ajaxUpdatePersonReadtime.action'
        data = {
            'cntindex': '2254283',
            'cntname': '带刺的朋友',
            'time': '2'
        }
        resp = self.session.post(url=url, data=data)
        print(self.mobile + ' ' + resp.text)

    def sendRightOfGoldCoin(self, sendTry=1, other_url=False):
        # 10010.woread.com.cn
        url = 'http://st.woread.com.cn/touchextenernal/readActivity/sendRightOfGoldCoin.action?userType=112&homeArea=036&homeCity=360&sendType=2'
        if other_url:
            url = 'http://st.woread.com.cn/touchextenernal/readActivity/sendRightOfGoldCoin.action?userType=112&homeArea=036&homeCity=360'
        resp = self.session.get(url=url)
        print(self.mobile + ' ' + resp.text)
        data = resp.json()
        if data['innercode'] == '2002':  # 今日已完成
            return 0
        if data['innercode'] == '2003':  # 无库存(120、100)
            return 0
        if data['innercode'] == '2004':  # 阅读时长不够
            pass
        if data['innercode'] == '2008':  # 无库存(120/100)
            other_url = True
        if data['innercode'] != '0000' and sendTry > 0:  # 额外增加阅读时长
            self.flushTime(120)
            self.ajaxUpdatePersonReadtime()
            self.sendRightOfGoldCoin(sendTry - 1, other_url)
        elif data['innercode'] != '0000' and sendTry <= 0:
            return 0
        else:
            data = resp.json()
            return data['message']['daySurplus']

    def checkRightOfGoldCoin(self):
        url = 'http://st.woread.com.cn/touchextenernal/readActivity/checkRightOfGoldCoin.action'
        resp = self.session.get(url=url)
        print(self.mobile + ' ' + resp.text)
        try:
            data = resp.json()
            return data['message']['ptimes'] + 1
        except:
            return 11

    def run(self):
        start = self.checkRightOfGoldCoin()
        if start == 11:
            return
        print(f'{self.mobile}第{start}次阅读'.center(64, '-'))
        self.flushTime(60)
        for _ in range(3):
            self.ajaxUpdatePersonReadtime()
            if _ < 2:
                self.flushTime(120)
            else:
                self.flushTime(randint(25, 30))
        self.sendRightOfGoldCoin()


if __name__ == "__main__":
    pass
