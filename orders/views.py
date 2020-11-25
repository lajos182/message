from rest_framework.views import APIView
from django.contrib.auth import authenticate
from notifications.signals import notify

from orders.consumers import send_group_msg
from orders.utils import lose_response, win_response


class UserInfoView(APIView):

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            return lose_response(message='账户名或密码错误')
        send_group_msg(service_uid=user, message='登录成功')
        return win_response(message='登录成功')