from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.users),
    # http://127.0.0.1:8000/v1/users/<username>
    # APPEND_SLASH = False 自動補全url後面的斜線，前提示你要有一個帶/的路由
    url(r'^/(?P<username>[\w]{1,55})$', views.users),
    # POSTMAN GET url測試
    # url(r'^/<username>', views.users),

]


