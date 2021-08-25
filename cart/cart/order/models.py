from django.db import models
from user.models import UserProfile
from commodity.models import Commodity
# Create your models here.

class Order(models.Model):

    o_id = models.AutoField(verbose_name='訂單ID', primary_key=True, auto_created=True)
    order_num = models.CharField(max_length=50, verbose_name='訂單編號')
    u_id = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    c_id = models.ForeignKey(Commodity,on_delete=models.CASCADE)
    o_num = models.IntegerField(verbose_name='訂單商品數量')
    create_time = models.DateTimeField(auto_now_add=True)
    # o_status 狀態編碼？ 1：尚未支付 2：已結帳
    o_status = models.IntegerField(verbose_name='訂單狀態')



    class Meta:
        db_table = 'order_file'
