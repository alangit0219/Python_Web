# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2021-08-02 09:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('commodity', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('o_id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='訂單ID')),
                ('order_num', models.CharField(max_length=50, verbose_name='訂單編號')),
                ('o_num', models.IntegerField(verbose_name='訂單商品數量')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('o_status', models.IntegerField(verbose_name='訂單狀態')),
                ('c_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commodity.Commodity')),
                ('u_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserProfile')),
            ],
            options={
                'db_table': 'order_file',
            },
        ),
    ]
