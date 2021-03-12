from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from notifications.signals import notify

from orders.consumers import send_group_msg
from orders.utils import lose_response, win_response


def IndexView(request):
    return render(request, 'index.html')



class UserInfoView(APIView):

    def get(self, request):
        send_group_msg('123', '订单已经收到了...')
        print('11111================')
        return win_response(message='get user info...')

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            return lose_response(message='账户名或密码错误')
        send_group_msg(service_uid=user, message='登录成功')
        return win_response(message='登录成功')