# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
def mail():
    host="smtp.aliyun.com"
    port=25
    sender="zfs9521@aliyun.com"
    pwd="xxxxxx"
    recv="1870658887@qq.com"
    mim=MIMEText("cpu boom","plain","utf-8")
    mim['subject']="cpu is boom"
    mim['from']=sender
    mim['to']=recv
#     mim['cc']=cc
    try:
        s=smtplib.SMTP(host,port)
        s.login(sender,pwd)
        s.sendmail(sender,recv,mim.as_string())
        print("mail success")
    except smtplib.SMTPException as e:
        print(e)
mail()

# # -*- coding: utf-8 -*-
# import smtplib
# from email.mime.text import MIMEText
# host="smtp.163.com"
# port=25
# sender="ttt_988@163.com"
# pwd="1qaz2wsx3edc"
# receiver="1870658887@qq.com"
# # body='<h1>this is test mail</h1>'
# f=open("report_test.html","rb")
# mail_body=f.read()
# f.close()
# 
# msg=MIMEText(mail_body,"html","utf-8")
# msg['subject']='this is report '
# msg['from']=sender
# msg['to']=receiver
# try:
#     s=smtplib.SMTP(host,port)
#     s.login(sender,"1qaz2wsx")
#     s.sendmail(sender,receiver,msg.as_string())
#     print("Done")
# except smtplib.SMTPException as e:
#     print(e)
