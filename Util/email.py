from appConfig import app
from flask_mail import Mail, Message

mail = Mail(app)


def send_email(to_address, cc_address, subject, body, html, attachments="none"):
    msg = Message(subject, recipients=[to_address], sender=(app.config['MAIL_SENDER'], "me@example.com"))
    msg.body = body
    msg.html = html
    if attachments != "none":
        with app.open_resource(attachments) as fp:
            msg.attach("image.jpg", "image/jpg", fp.read())
    mail.send(msg)
