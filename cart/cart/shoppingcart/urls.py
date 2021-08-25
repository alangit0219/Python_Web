from django.conf.urls import url
from . import views

urlpatterns =[
    url(r'^$', views.get_cart),
    url(r'^/(?P<commodity_id>[\w]{1,11})$', views.carts),
    # url(r'^/(?P<usename>[\w]{1,11})/(?P<commodity_id>[\w]{1,11})$', views.carts),

]
