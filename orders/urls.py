from django.urls import re_path

from orders import views

urlpatterns = [
    re_path(r'^user/$', views.UserInfoView.as_view()),
    re_path(r'^chat/$', views.IndexView),
]
