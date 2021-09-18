import smtplib
import requests
from email.mime.text import MIMEText


class Message:

    def __init__(self, subject, content, msg_from, password, msg_to, token):
        self.content = content
        self.msg_from = msg_from
        self.password = password
        self.msg_to = msg_to
        self.token = token
        self.subject = subject
        self.session = requests.Session()
        self.session.headers = requests.structures.CaseInsensitiveDict({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
        })
        self.init_content()

    def init_content(self):
        template = ''
        for s in self.content.split('\n'):
            indent = s.count(' ')
            s = s.strip()
            template += f'<div style="margin-bottom: -10px;"><font size="1" face="黑体">{indent * "&nbsp; "}{s}</font></div>'
        self.content = template

    def qqemail(self):
        """
            QQ邮箱接收推送消息
            消息自己发给自己
        """
        msg = MIMEText(self.content, 'html')  # 生成一个MIMEText对象
        msg['subject'] = self.subject  # 放入邮件主题
        msg['from'] = self.msg_from  # 放入发件人
        msg['to'] = self.msg_to  # 放入收件人
        try:
            # 通过ssl方式发送，服务器地址，端口
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            # 登录到邮箱
            s.login(self.msg_from, self.password)
            # 发送邮件 发送方 收件方 要发送的消息
            s.sendmail(self.msg_from, self.msg_to, msg.as_string())
            # 关闭会话
            s.quit()
        except smtplib.SMTPException as e:
            print(e)

    def pushplus(self):
        """
            utils/config.py 消息推送配置
            微信扫码登录 http://www.pushplus.plus/
            一对一推送 复制自己的token
            pushplus微信公众号接收推送消息
        """
        try:
            url = 'http://www.pushplus.plus/api/send'
            data = {
                "channel": "wechat",
                "content": self.content,
                "template": "html",
                "title": self.subject,
                "token": self.token,
                "webhook": ""
            }
            resp = requests.post(url, json=data, headers={
                'Content-Type': 'application/json'
            })
            print(resp.json())
        except Exception as e:
            print(e)

    def run(self):
        if self.token:
            self.pushplus()
        if self.msg_from and self.password and self.msg_to:
            self.qqemail()


def getMessage(content):
    from utils.config import push_message_conf
    return Message('联通每日任务', content, **push_message_conf)


if __name__ == "__main__":
    pass
