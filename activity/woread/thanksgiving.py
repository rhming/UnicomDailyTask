# -*- coding: utf8 -*-
import time
from lxml import etree
from random import choice
from activity.woread.flowdraw import WoRead


class ThanksGiving(WoRead):

    def __init__(self, mobile, _=None):
        super(ThanksGiving, self).__init__(mobile)
        self.session.headers.update({
            "Referer": "https://st.woread.com.cn/touchextenernal/thanksgiving/index.action",
        })

    def index(self):
        url = 'https://st.woread.com.cn/touchextenernal/thanksgiving/goldegg.action'
        data = {
            "allactiveindex": "MDMzMURDNTNDQzA0RDk5QTQ2RTI1RkQ5OEYwQzQ2RkI=",
        }
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        cookies = resp.cookies.get_dict()
        if cookies.get('JSESSIONID', False):
            self.saveCookie(f'{self.mobile}WoRead', self.session.cookies.get_dict())
        e = etree.HTML(resp.text)
        drawNum = int(e.xpath('string(//span[@id="drawNum_id"]/text())'))
        return drawNum

    def getIntellectRecommend(self):
        url = 'https://st.woread.com.cn/touchextenernal/read/getIntellectRecommend.action'
        data = {
            "recommendid": "0",
            "cntsize": "6",
            "recommendsize": "1"
        }
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        result = resp.json()
        data = [
            [item['cntname'], item['cntindex']] for item in result['message']['catlist']
        ]
        book = choice(data)
        return book[1]

    def reportLatestRead(self, item):
        url = 'https://st.woread.com.cn/touchextenernal/contentread/reportLatestRead.action'
        data = {
            "cntindex": item['cntindex'],
            "chapterallindex": item['chapterallindex'],
            "catindex": item['catindex'],
            "cnttype": item['cnttype'],
            "cntname": item['cntname'],
            "cntrarflag": item['cntrarflag'],
            "chapterseno": item['chapterseno'],
            "chaptertitle": item['curChapterTitle'].replace(' ', '+'),
            "authorname": item['authorname'],
            "iconFile": "",
            "volumeallindex": item['volumeallindex'],
            "finishflag": "1"
        }
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        print(resp.json())

    def newRead(self, cntindex):
        url = "https://st.woread.com.cn/touchextenernal/read/newRead.action"
        data = {
            "cntindex": cntindex
        }
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        result = resp.json()
        print(result)
        if result['message']:
            return int(result['message']['chapterseno']) + 1
        return 1

    def ajaxchapter(self, item):
        url = 'https://st.woread.com.cn/touchextenernal/contentread/ajaxchapter.action'
        params = {
            "cntindex": item['cntindex'],
            "catid": "",
            "volumeallindex": item['volumeallindex'],
            "chapterallindex": item['chapterallindex'],
            "chapterseno": item['chapterseno'],
            "activityID": "",
            "pageIndex": "",
            "cardid": "",
            "_": self.server_timestamp,
        }
        resp = self.session.get(url=url, params=params)
        resp.encoding = 'utf8'
        result = resp.json()
        result['contentInfo'] = ''
        result['listPreNextJSONArray'] = ''
        # print(result)
        return resp.json()

    def getUpDownChapter(self, cntindex, chapterseno=1):
        url = "https://st.woread.com.cn/touchextenernal/read/getUpDownChapter.action"
        data = {
            "cntindex": cntindex,
            "chapterseno": str(chapterseno)
        }
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        result = resp.json()
        for item in result['message']:
            if int(item['chapterseno']) == chapterseno:
                # print(item)
                return item

    def doDraw(self):
        """
        抽奖
        """
        url = 'https://st.woread.com.cn/touchextenernal/thanksgiving/doDraw.action'
        data = {
            "acticeindex": "MDMzMURDNTNDQzA0RDk5QTQ2RTI1RkQ5OEYwQzQ2RkI="
        }
        resp = self.session.post(url=url, data=data)
        result = resp.json()
        try:
            log = f'{self.now_time}_thanksgiving_{result["prizedesc"]}'
            self.recordLog(log)
        except:
            print(result)

    def run(self):
        try:
            drawNum = self.index()
            if not drawNum:
                cntindex = self.getIntellectRecommend()
                for _ in range(1, 11):
                    # cntindex = '1840947'
                    chapterseno = _
                    # chapterseno = self.newRead(cntindex)
                    item = self.getUpDownChapter(cntindex, chapterseno)
                    item = self.ajaxchapter(item)
                    print(f"正在阅读<{item['cntname']}>-<{item['curChapterTitle']}>...")
                    self.reportLatestRead(item)
                    self.flushTime(12)
            drawNum = self.index()
            if drawNum:
                self.doDraw()
            else:
                print('抽奖机会已用完')
        except Exception as e:
            print(e)


if __name__ == "__main__":
    pass
