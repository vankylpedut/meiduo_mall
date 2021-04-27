import logging

from django_redis import get_redis_connection
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from celery_tasks.sms.tasks import send_sms_code

logger = logging.getLogger('django')


class SmsCodeView(APIView):
    def get(self, request, mobile):
        # 获取StrictRedis保存数据
        strict_redis = get_redis_connection('sms_codes')

        # 4、60秒内禁止重复发送短信验证码
        send_flag = strict_redis.get('sms_flag_%s' % mobile)
        if send_flag:
            raise ValidationError({'message': '禁止重复发送短信验证码'})

        # 1、生成短信验证码
        import random
        sms_code = '%06d' % random.randint(0, 999999)
        logger.info('获取的验证码为:%s' % sms_code)
        # 2、使用云通信发送短信验证码
        # CCP().send_template_sms(mobile, [sms_code, 5], 1)

        # 3、保存短信验证码到Redis expiry
        # strict_redis = get_redis_connection('sms_codes')
        pipeline = strict_redis.pipeline()  # Pipeline类

        # sms_13600000001        111111      （验证码：5分钟过期）
        # strict_redis.setex('sms_%s' % mobile, 5 * 60, sms_code)  # 5min
        # pipeline.setex('sms_%s' % mobile, 60 * 5, sms_code)
        send_sms_code.delay(mobile, sms_code)

        # send_flag_13600000001       1      （发送标识：1分钟过期）
        # strict_redis.setex('sms_flag_%s' % mobile, 60, 1)
        pipeline.setex('sms_flag_%s' % mobile, 60, True)

        result = pipeline.execute()
        print(result)

        # 5、响应数据
        return Response({'message': 'OK'})
