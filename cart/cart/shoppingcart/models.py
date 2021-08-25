from django.db import models
from user.models import UserProfile
from commodity.models import Commodity
# Create your models here.

class ShoppingCart(models.Model):

    car_id = models.AutoField(verbose_name='購物車ID', primary_key=True, auto_created=True)
    u_id = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    c_id = models.ForeignKey(Commodity,on_delete=models.CASCADE)
    num = models.IntegerField(verbose_name='數量')
    # c_status 狀態編碼 1:正常 2:禁止使用 3:刪除
    c_status = models.IntegerField(verbose_name='購物車狀態')

    class Meta:
        db_table = 'shoppingcart'
