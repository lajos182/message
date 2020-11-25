from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class UserInfo(AbstractUser):
    phone = models.CharField(max_length=11, help_text='手机号码')
    first_name = None
    last_name = None


class Order(models.Model):
    userinfo = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    order_number = models.CharField(max_length=32, help_text='订单编号')
    order_state = models.BooleanField(default=False, help_text='订单状态')
    create_date = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    update_date = models.DateTimeField(auto_now=True, help_text='更新时间')
