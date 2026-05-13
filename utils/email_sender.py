from flask_mail import Message
from flask import current_app, url_for

def send_verification_email(mail, user_email, token):
    verification_url = url_for('auth.verify_email', token=token, _external=True)
    msg = Message('Verify your email address',
                  recipients=[user_email])
    msg.body = f'''Hello,

Please click the link below to verify your email address:
{verification_url}

If you did not request this, please ignore this email.
'''
    mail.send(msg)
