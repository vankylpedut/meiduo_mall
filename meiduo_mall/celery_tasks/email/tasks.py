from time import sleep

from celery_tasks.main import celery_app
from celery_tasks.sms.yuntongxun.sms import CCP


@celery_app.task
def send_email_code(email, email_code):
    sleep(5)
    print('发送邮箱验证码', email_code)
