from django.conf.urls import url

from verifications import views

urlpatterns = [
    # 发送短信验证码配置url
    url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$',
        views.SmsCodeView.as_view()),
]
