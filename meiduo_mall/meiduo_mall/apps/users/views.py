from django.conf import settings
from django.shortcuts import render

# Create your views here.
from django.views import View
from itsdangerous import BadData
from itsdangerous import TimedJSONWebSignatureSerializer
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken

from meiduo_mall.utils.exceptions import logger
from users import serializers
from users.models import User


class TestView(View):
    def get(self, request):
        return render(request, 'test.html')


# test2/
class TestView2(APIView):
    def get(self, request):
        response = Response({'message': 'get请求'})
        # response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8080'
        return response

    def post(self, request):
        response = Response({'message': 'post请求'})
        # response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8080'
        return response


class UsernameCountView(APIView):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()

        data = {
            "username": username,
            "count": count
        }

        return Response(data)


class PhoneCountView(APIView):
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()

        data = {
            "mobile": mobile,
            "count": count
        }

        return Response(data)


class CreateUserView(CreateAPIView):
    '''用户注册'''
    serializer_class = serializers.CreateUserSeriliazer


class MyObtainJSONWebToken(ObtainJSONWebToken):
    '''登陆接口'''
    pass


class UserDetailView(RetrieveAPIView):
    serializer_class = serializers.UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class EmailView(UpdateAPIView):
    '''修改用户邮箱（修改用户的邮箱字段）'''
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.EmailSerializer

    # 重写GenericAPIView的方法，指定要修改的是哪一条用户数据
    def get_object(self):
        return self.request.user


class VerifyEmailView(APIView):
    '''激活用户邮箱'''

    def get(self, reuqest):
        '''获取token值'''
        token = reuqest.query_params.get('token')
        if not token:
            return Response({'message': '缺失token值'})

        # 验证token
        s = TimedJSONWebSignatureSerializer(
            settings.SECRET_KEY, expires_in=60 * 60 * 24)  # 有效期1天
        try:
            # 进行解密
            data = s.loads(token)
        except BadData:
            return Response({'message': '链接信息无效'}, status=400)

        # 查询要激活的用户
        email = data.get('email')
        user_id = data.get('user_id')

        # 获取要激活的用户
        try:
            user = User.objects.get(user_id=user_id, email=email)
        except:
            return Response({'message': '激活用户不存在'})

        # 如果用户存在，修改用户的激活状态
        user.email_active = True
        # 执行修改动作
        user.save()

        return Response({'message': 'OK'})
