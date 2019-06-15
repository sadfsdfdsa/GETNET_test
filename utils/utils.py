import smtplib


def email_sender(input_message, email_to):
    gmail_user = 'shuvaevartem2001@gmail.com' # input ur infos, this examples can be failed!
    gmail_pwd = 'a04042001unholy' # input ur infos, this examples can be failed!
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login(gmail_user, gmail_pwd)
    header = 'To:' + email_to + '\n' + 'From: ' + gmail_user + '\n' +'Authorization in Shuvaev App \n'
    input_message = input_message
    msg = header + input_message
    smtpserver.sendmail(gmail_user, email_to, msg)
    smtpserver.close()
