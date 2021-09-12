# -*- coding: utf8 -*-
import re
from lxml import etree
from activity.woread.flowdraw import WoRead


class ReadLuchDraw(WoRead):

    def __init__(self, mobile, _=None):
        super(ReadLuchDraw, self).__init__(mobile)
        self.session.headers.update({
            "Referer": "https://st.woread.com.cn/touchextenernal/readluchdraw/index.action",
        })
        self.isdrawtoday = False

    def index(self):
        url = 'https://st.woread.com.cn/touchextenernal/readluchdraw/goldegg.action'
        resp = self.session.post(url=url)
        cookies = resp.cookies.get_dict()
        if cookies.get('JSESSIONID', False):
            self.saveCookie(f'{self.mobile}WoRead', self.session.cookies.get_dict())

        e = etree.HTML(resp.text)
        if e.xpath("//div[@class='cardStateTex']/span/text()")[2].find("今日 已打卡") > -1:
            self.isdrawtoday = True

        cardList = e.xpath("//div[@class='cardBtn noCarded']/div[2]/@onclick")

        for cardText in cardList:
            # print(cardText)
            if cardText.find('fillDrawTimes') == -1:
                continue
            date_string = re.findall(
                r".+fillDrawTimes\('(\d+)'.+", cardText
            )[0]
            # print(date_string)
            self.fillDrawTimes(date_string)
            self.flushTime(20)

    def fillDrawTimes(self, date_string):
        """
        date_string 20210601
        补签
        """
        print(f'{date_string}补签')
        url = f'https://st.woread.com.cn/touchextenernal/readluchdraw/fillDrawTimes.action?date={date_string}'
        resp = self.session.get(url=url)
        print(resp.json())

    def addDrawTimes(self):
        """
        打卡
        """
        url = 'http://st.woread.com.cn/touchextenernal/readluchdraw/addDrawTimes.action'
        resp = self.session.post(url=url)
        print(resp.json())

    def doDraw(self, acticeindex):
        """
        抽奖
        """
        url = 'https://st.woread.com.cn/touchextenernal/readluchdraw/doDraw.action'
        data = {
            "acticeindex": acticeindex
        }
        resp = self.session.post(url=url, data=data)
        result = resp.json()
        print(result)
        log = f'{self.now_time}_readluchdraw_{result["prizedesc"]}'
        self.recordLog(log)

    def run(self):
        try:
            self.index()
            if not self.isdrawtoday:
                self.addDrawTimes()
            for acticeindex in [
                "QjUxRUZCMURBRUUyMzM2NTgwNUY2NzZGRTgxRUZGQUQ=",  # //一次 看视频20日流量
                "NzFGQzM2Mjc4RDVGNUM4RTIyMzk4MkQ3OUNEMkZFOUE=",  # //默认
                "OTJGMDkwNjk0Mjc4MjU2MkQyQjIyMzRGRDRGQzk4MzA=",  # //额外
            ]:
                print(f'{self.mobile}抽奖-{acticeindex}')
                self.doDraw(acticeindex)
                self.flushTime(3)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    pass
