import json
from urllib.parse import unquote
from utils.common import Common
from utils.message import getMessage


class PushLog(Common):

    def __init__(self, accounts, _=None):
        super(PushLog, self).__init__()
        self.accounts = accounts
        self.message = ''

    def run(self):
        for account in self.accounts:
            account = unquote(account)
            self.mobile = account
            for record in ['SigninAppRecord', 'WoReadRecord', 'WoLearnRecord', 'WoMailRecord', 'WatchAddFlowRecord']:
                if account.isdigit() and record == 'WoMailRecord':
                    continue
                if not account.isdigit() and record != 'WoMailRecord':
                    continue
                self.message += f'{account}{record}[{self.now_date}]'.center(64, '-') + '\n'
                msg = self.readCookie(f'{account}{record}')
                if not msg:
                    msg = "未获取到日志"
                if isinstance(msg, dict):
                    msg = msg.get(self.now_date, '')
                    if not isinstance(msg, str):
                        msg = json.dumps(msg, indent=4, ensure_ascii=False)
                self.message += msg + '\n'
        getMessage(self.message).run()


if __name__ == '__main__':
    pass
