import logging
from threading import Thread

from src.app import app
from flask_mail import Message
from flask_mail import Mail
from flask import render_template

mail = Mail(app)


def send_message(**kwargs):
    msg = Message(**kwargs)

    with app.app_context():
        mail.send(msg)


def send_email_link(email, link, recipient=''):
    try:
        template_data = {
            "sender": "LTLB",
            "recipient": recipient,
            "message": "Вы успешно зарегистрировались. Для подтверждения почта, перейдите по ссылке ниже.",
            "link": {
                "url": link,
                "message": 'Follow link'
            },
            "contacts": {
                "email": "admin@gmail.com",
                "phone": '+37360000000'
            }
        }

        body = render_template('email_templates/register.html', data=template_data)

        data = {
            "html": body,
            "subject": 'Email Verification',
            "recipients": [email],
            "sender": "noreply@gmail.com",
        }
        my_thread = Thread(target=send_message, kwargs=data)
        my_thread.start()
    except Exception as e:
        logging.error(e)


def send_forgot_password_email(email, link, recipient=''):
    template_data = {
        "sender": "LTLB",
        "recipient": recipient,
        "message": "Вы пытаетесь восстоноваить доступ к вашему аккаунте. Что бы подтвердить действия, перейдите по ссыоке ниже",
        "link": {
            "url": link,
            "message": 'Восстановить пароль'
        },
        "contacts": {
            "email": "admin@gmail.com",
            "phone": '+37360000000'
        }
    }

    body = render_template('email_templates/template.html', data=template_data)
    data = {
        "html": body,
        "subject": 'Forgot password',
        "recipients": [email],
        "sender": "noreply@gmail.com",
    }
    my_thread = Thread(target=send_message, kwargs=data)
    my_thread.start()


def send_info_email(**kwargs):
    template_data = {
        "sender": "LTLB",
        "recipient": kwargs.get('name', ''),
        "message": kwargs.get('message', ''),
        "link": kwargs.get('link', ''),
        "contacts": {
            "email": "admin@gmail.com",
            "phone": '+3736000000'
        }
    }

    body = render_template('email_templates/template.html', data=template_data)
    recipients = kwargs.get('recipient', [])

    if type(recipients) != 'list':
        recipients = [recipients]

    data = {
        "html": body,
        "subject": kwargs.get('subject', ''),
        "recipients": recipients,
        "sender": "noreply@gmail.com",
    }

    my_thread = Thread(target=send_message, kwargs=data)
    my_thread.start()
