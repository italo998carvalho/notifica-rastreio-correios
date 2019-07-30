import smtplib
import ssl
from config import sender_email
from config import sender_password
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
    
class MailSender:
    def __init__(self, message, receiver_email):
        self.message = message
        self.receiver_email = receiver_email

        self.msg = MIMEMultipart()

        self.sender_email = sender_email
        self.sender_password = sender_password

        self.server = smtplib.SMTP('smtp.gmail.com: 587')

    def send(self):
        self.server.starttls()
        self.server.login(self.sender_email, self.sender_password)

        message = f'Subject: Atualização no envio do seu pacote\n{self.message}'
        self.msg.attach(MIMEText(message, 'plain'))

        self.server.sendmail(self.sender_email, self.receiver_email, message.encode('utf-8'))

        self.server.quit()