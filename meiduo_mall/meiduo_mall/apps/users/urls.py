from django.conf.urls import url

from meiduo_mall.apps.users import views

# from users import views

urlpatterns = [
    url(r'^test/$', views.TestView.as_view()),
    url(r'^test2/$', views.TestView2.as_view()),
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
]
