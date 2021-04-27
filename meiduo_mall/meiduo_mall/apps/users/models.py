from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):  # 继承父类，添加自定义字段，不用挨个定义，继承父类+添加自定义字段

    """用户模型类"""
    # mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    # 手机号码本来要限制unique字段的，但为了方便测试，暂时不用，后期上线，再补回去
    mobile = models.CharField(max_length=11, verbose_name='手机号')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
