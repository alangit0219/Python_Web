from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.categorys),
    # http://127.0.0.1:8000/v1/commodity
    # APPEND_SLASH = False 自動補全url後面的斜線，前提示你要有一個帶/的路由
    # url(r'^/(?P<category>[\w]{1,55})$', views.categorys),
    url(r'^/(?P<c_id>[\w]{1,55})$', views.commoditys),
    # POSTMAN GET url測試
    # url(r'^/<category>', views.categorys),
    # url(r'^/<commodityname>', views.commoditys),

]


