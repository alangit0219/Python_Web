from django.conf.urls import url
from . import views

urlpatterns = [

    # http://127.0.0.1:8000/v1/orders
    # APPEND_SLASH = False 自動補全url後面的斜線，前提示你要有一個帶/的路由
    url(r'^/total_check$', views.total_check),
    url(r'^/capture_order_id$', views.capture_order_id),
    url(r'^/(?P<order_num>[\w]{1,55})$', views.order_detail),
    url(r'^$', views.orders),

]


