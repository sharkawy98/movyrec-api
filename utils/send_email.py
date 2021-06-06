from flask_mail import Mail, Message

mail = Mail()

def send_email(to_email, subject, body):
    msg = Message(
        subject,
        sender='movyrek@gmail.com',
        recipients=[to_email],
        html=body
    )
    mail.send(msg)