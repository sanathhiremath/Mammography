from appConfig import app
from flask_mail import Mail, Message

mail = Mail(app)


def send_email(to_address, cc_address, subject, body, html):
    msg = Message(subject, recipients=[to_address], sender=(app.config['MAIL_SENDER'], "me@example.com"))
    msg.body = body
    msg.html = html
    mail.send(msg)
