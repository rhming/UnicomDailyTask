# -*- coding: utf8 -*-
from random import choice, randint
from activity.woread.flowdraw import WoRead


class ReadBook(WoRead):

    def __init__(self, mobile, _=None):
        super(ReadBook, self).__init__(mobile)
        self.session.headers.update({
            "Referer": "https://st.woread.com.cn/touchextenernal/thanksgiving/index.action",
        })

    def getIntellectRecommend(self):
        url = 'https://st.woread.com.cn/touchextenernal/read/getIntellectRecommend.action'
        data = {
            "recommendid": "0",
            "cntsize": "24",
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

    def run(self):
        if int(self.now_date.replace('-', '')) > 20220228:
            return
        try:
            cntindex = self.getIntellectRecommend()
            start = randint(1, 50)
            for _ in range(start, start + 15):
                try:
                    chapterseno = _
                    item = self.getUpDownChapter(cntindex, chapterseno)
                    item = self.ajaxchapter(item)
                    print(f"正在阅读<{item['cntname']}>-<{item['curChapterTitle']}>...")
                    self.reportLatestRead(item)
                except:
                    pass
                self.flushTime(randint(8, 12))
        except Exception as e:
            print(e)


if __name__ == "__main__":
    pass
