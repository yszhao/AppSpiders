#coding:utf-8 #强制使用utf-8编码格式
import smtplib  #加载smtplib模块
from email.mime.text import MIMEText
from email.utils import formataddr
my_sender = 'yongshengfree@163.com' #发件人邮箱账号，为了后面易于维护，所以写成了变量
mailTo = ['xuxia@softsec.com.cn', 'zhaoyongsheng@softsec.com.cn'] #收件人邮箱账号，为了后面易于维护，所以写成了变量

def mail(subject, content):
    ret = True
    try:
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = formataddr(["实验室测试", my_sender])
        msg['To'] = formataddr(["许霞,赵永胜", mailTo])
        msg['Subject'] = subject #邮件的主题，即标题
        
        server = smtplib.SMTP("smtp.163.com", 25) #发件人邮箱的SMTP服务器，端口是25
        server.login(my_sender, "Zdd1258") #发件人邮箱账号，密码
        server.sendmail(my_sender, mailTo, msg.as_string()) #发件人账号，收件人账号列表，邮件内容
        server.quit() #关闭连接
        
    except Exception, e: #如果try中的语句没有执行，则会执行下面的ret=false
        ret = False
        print Exception, ":", e
    return ret

if __name__ == '__main__':
    subject = "测试邮件"
    msg = "测试一下"
    ret = mail(subject, msg)
    if ret:
        print("ok") #如果发送成功则会返回ok，稍等20秒左右就可以收到邮件
    else:
        print("failed") #如果发送失败则会返回failed
