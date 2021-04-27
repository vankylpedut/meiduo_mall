from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from meiduo_mall.utils.exceptions import logger
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
