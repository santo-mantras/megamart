from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = 'localhost'
SMTP_PORT = 1025
SENDER_EMAIL = '21f1000243@ds.study.iitm.ac.in'
SENDER_PASSWORD = ''

def send_message(to, subject, content_body):
    msg = MIMEMultipart()
    msg["To"] = to
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg.attach(MIMEText(content_body, 'plain'))
    client = SMTP(host= SMTP_HOST, port = SMTP_PORT)
    client.send_message(msg=msg)
    client.quit()
#send_message("sam@war.com","Daily Reminder","Two")