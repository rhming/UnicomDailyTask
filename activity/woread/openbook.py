# -*- coding: utf8 -*-
import re
from random import choice
from activity.woread.flowdraw import WoRead


class OpenBook(WoRead):

    def __init__(self, mobile, _=None):
        super(OpenBook, self).__init__(mobile)
        self.session.headers.update({
            'Referer': 'https://st.woread.com.cn/touchextenernal/openbook/index.action?channelid=18566059'
        })

    def index(self):
        url = 'https://st.woread.com.cn/touchextenernal/openbook/index.action?channelid=18566059'
        resp = self.session.get(url=url)
        resp.encoding = 'utf8'
        cookies = resp.cookies.get_dict()
        if cookies.get('JSESSIONID', False):
            self.saveCookie(f'{self.mobile}WoRead', self.session.cookies.get_dict())

        self.categoryList = re.findall(r'cateIds.push\((\d+)\);', resp.text)
        drawNum = re.findall(r'var drawNum = (\d);', resp.text)[0]
        drawNum = int(drawNum)
        currentSeevideoNum = re.findall(
            r'var currentSeevideoNum = (-?\d);', resp.text
        )[0]
        currentSeevideoNum = int(currentSeevideoNum)
        return drawNum, currentSeevideoNum

    def addUserSeeVideo(self, drawNum):
        url = f'https://st.woread.com.cn/touchextenernal/openbook/addUserSeeVideo.action?num={drawNum}&activityindex=RUEyODEwMzkxQ0E1RTZGQTE0NUNGNTM2Nzk1M0NCMEM='
        resp = self.session.get(url=url)
        print(resp.json())

    def doDraw(self, num):
        category = choice(self.categoryList)
        url = 'https://st.woread.com.cn/touchextenernal/openbook/doDraw.action'
        data = {
            'categoryId': category,
            'currentNum': '%d' % num
        }
        resp = self.session.post(url=url, data=data)
        result = resp.json()
        result['bookInfo'] = ''
        print(result)

        log = f'{self.now_time}_openbook_{category}_{result["prizedesc"]}'
        self.recordLog(log)

    def run(self):
        try:
            drawNum, currentSeevideoNum = self.index()
            if currentSeevideoNum == -1 and drawNum < 3:
                self.addUserSeeVideo(str(drawNum))
                drawNum, currentSeevideoNum = self.index()
            if drawNum == 0:
                print('抽奖次数已用完...')
                return
            print(f'#bookdraw#第{6 - drawNum}次抽奖...')
            self.doDraw(6 - drawNum)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    pass
