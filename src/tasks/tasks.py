import smtplib
import ssl
from email.message import EmailMessage

from celery import Celery
from config import SMTP_USER, SMTP_PASSWORD

SMTP_HOST = 'smtp.yandex.ru'
SMTP_PORT = 465

celery = Celery('tasks', broker="redis://localhost:6379")


def get_email_temleate_dashboard(username: str):
    email = EmailMessage()
    email['Subject'] = 'Отчёт'
    email['From'] = SMTP_USER
    email['To'] = 'megajeiksteam@gmail.com'

    email.set_content(
        '<div>'
        f'<h1 style="color: red;">Здравствуйте, {username}, а вот и ваш отчет. Зацените 😊  ТЫ ПИДОР ! </h1>'
        '<img src="https://static.vecteezy.com/system/resources/previews/008/295/031/original/custom-relationship'
        '-management-dashboard-ui-design-template-suitable-designing-application-for-android-and-ios-clean-style-app'
        '-mobile-free-vector.jpg" width="600">'
        '</div>',
        subtype='html'
    )
    return email


@celery.task
def send_email_report_dashboard(username: str):
    email = get_email_temleate_dashboard(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
