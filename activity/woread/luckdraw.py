# -*- coding: utf8 -*-
import re
from activity.woread.flowdraw import WoRead


class LuckDraw(WoRead):

    def __init__(self, mobile, _=None):
        super(LuckDraw, self).__init__(mobile)
        self.session.headers.update({
            'Referer': 'http://st.woread.com.cn/touchextenernal/seeadvertluckdraw/index.action?channelid=18000687',
        })

    def index(self):
        url = f'http://st.woread.com.cn/touchextenernal/seeadvertluckdraw/index.action?channelid=18000687'
        resp = self.session.get(url=url)
        resp.encoding = 'utf8'

        cookies = resp.cookies.get_dict()
        if cookies.get('JSESSIONID', False):
            self.saveCookie(f'{self.mobile}WoRead', self.session.cookies.get_dict())

        drawNum = re.findall(r'var drawNum = (\d);', resp.text)[0]
        drawNum = int(drawNum)
        currentSeevideoNum = re.findall(
            r'var currentSeevideoNum = (-?\d);', resp.text
        )[0]
        currentSeevideoNum = int(currentSeevideoNum)
        return drawNum, currentSeevideoNum

    def addUserSeeVideo(self, drawNum):
        url = f'https://st.woread.com.cn/touchextenernal/openbook/addUserSeeVideo.action?num={drawNum}&activityindex=NzJBQTQxMEE2QzQwQUE2MDYxMEI5MDNGQjFEMEEzODI='
        resp = self.session.get(url=url)
        print(resp.json())

    def doDraw(self, acticeindex):
        url = 'http://st.woread.com.cn/touchextenernal/seeadvertluckdraw/doDraw.action'
        '''
                5-21(over): jRFMzZCMEM0MjJGRjZFMkQ3RUVFN0ZERTEyQUI4MTc=
                6-21(over): QjRFMzZCMEM0MjJGRjZFMkQ3RUVFN0ZERTEyQUI4MTc=
                6-21(start): NzJBQTQxMEE2QzQwQUE2MDYxMEI5MDNGQjFEMEEzODI=
        '''
        data = {
            'acticeindex': acticeindex
        }
        # data['acticeindex'] = 'jRFMzZCMEM0MjJGRjZFMkQ3RUVFN0ZERTEyQUI4MTc='
        resp = self.session.post(url=url, data=data)
        print(acticeindex + ' ' + resp.text)
        result = resp.json()
        log = f'{self.now_time}_luckdraw_{result["prizedesc"]}'
        self.recordLog(log)

    def run(self):
        try:
            drawNum, currentSeevideoNum = self.index()
            if currentSeevideoNum == -1 and drawNum < 2:
                self.addUserSeeVideo(str(drawNum))
                drawNum, currentSeevideoNum = self.index()
            if drawNum == 0:
                print('抽奖次数已用完...')
                return
            print(f'#luckdraw#第{6 - drawNum}次抽奖...')
            self.doDraw('NzJBQTQxMEE2QzQwQUE2MDYxMEI5MDNGQjFEMEEzODI=')
            if drawNum == 2:
                self.flushTime(3)
                self.doDraw('QjRFMzZCMEM0MjJGRjZFMkQ3RUVFN0ZERTEyQUI4MTc=')
        except Exception as e:
            print(e)


if __name__ == "__main__":
    pass
