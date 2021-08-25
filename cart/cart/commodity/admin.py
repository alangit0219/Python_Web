from django.contrib import admin

# Register your models here.
from . import models
class CommidityManager(admin.ModelAdmin):
    list_display = ['commodity_id','commodityname', 'category', 'price',
                    'quantity', 'c_photo']
    list_display_links = ['commodity_id','commodityname']
    list_filter = ['category']
    search_fields = ['commodity_id','commodityname', 'category']
    list_editable = ['category', 'price', 'quantity']

admin.site.register(models.Commodity,CommidityManager)