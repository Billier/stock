import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send(msg):
    from_address = '1132967155@qq.com'
    to_address = ['179756968@qq.com']

    try:
        smtpObj = smtplib.SMTP_SSL("smtp.qq.com", 465)
        # smtpObj.set_debuglevel(1)
        message = MIMEText(msg, _charset='utf-8')
        message['Subject'] = Header('温馨提醒', 'utf-8')
        message['From'] = Header("Robert", 'utf-8')
        message['To'] = Header("大哥", 'utf-8')
        smtpObj.login(from_address, "jtuykkvnwqyobaag")
        smtpObj.sendmail(from_address, to_address, message.as_string())
        print("邮件发送成功")
        smtpObj.quit()

    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


if __name__ == "__main__":
    send("Python 邮件发送测试...")
