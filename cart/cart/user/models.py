from django.db import models

# Create your models here.

class UserProfile(models.Model):

    user_id = models.AutoField(verbose_name='用戶ID',primary_key=True,auto_created=True)
    username = models.CharField(max_length=12, verbose_name='用戶名')
    email = models.EmailField(max_length=250, verbose_name='信箱')
    password = models.CharField(max_length=32, verbose_name='密碼')
    phone = models.CharField(max_length=11, verbose_name='電話')
    address = models.CharField(max_length=50, verbose_name='地址', null=True)

    class Meta:
        db_table = 'user_profile'
