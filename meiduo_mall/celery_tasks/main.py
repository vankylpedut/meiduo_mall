import os

# 1、设置配置文件，需要放置到创建celery对象之前
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings.dev")

# 2、参数1：自定义的一个名字
# celery_app = Celery('meiduo', broker='redis://127.0.0.1:6379/15', backend='redis://127.0.0.1:6379/14')

#  方法2
celery_app = Celery('meiduo')
celery_app.config_from_object('celery_tasks.config')

# 3、指定要扫描的任务的包，会自动读取包下名字为tasks.py的文件
celery_app.autodiscover_tasks(['celery_app.sms', 'celery_app.email'])
