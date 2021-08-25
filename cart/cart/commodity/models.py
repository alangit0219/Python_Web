# commoiditys_models.py 商品區塊模型

from django.db import models
# Create your models here.

class Commodity(models.Model):
    commodity_id = models.AutoField(verbose_name='商品ID', primary_key=True, auto_created=True)
    commodityname = models.CharField(max_length=20, verbose_name='商品名稱')
    # 'coffee'-咖啡豆類 'cup'-濾杯類 'machine'-咖啡機器類
    category = models.CharField(max_length=20, verbose_name='商品分類')
    price = models.IntegerField(verbose_name='商品價格')
    quantity = models.IntegerField(verbose_name='商品數量')
    c_content = models.TextField(max_length=100,verbose_name='商品說明')
    c_photo = models.ImageField(upload_to='photo/',null=True)

    class Meta:
        db_table = 'commodity'
