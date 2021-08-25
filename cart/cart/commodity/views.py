import datetime
from django.db.models.fields.files import ImageFieldFile
from django.http import JsonResponse
from django.shortcuts import render
from .models import *

# Create your views here.
def categorys(request, category=None):
    if request.method == 'GET':
        if category:
            # 分類區分 coffee='1' cup='2' machine='3'
            categorys = Commodity.objects.filter(category=category)
            if not categorys:
                result = {'code': 401, 'error': 'Category is not exist!'}
                return JsonResponse(result)
            result = make_commoditys_result(categorys)
            return JsonResponse(result)

        # 獲取所有商品
        commoditys = Commodity.objects.all().order_by('-commodity_id')
        if not commoditys:
            result = {'code': 500, 'error': 'System Error try again'}
            return JsonResponse(result)
        # 商品序列化
        result = make_commoditys_result(commoditys)
        return JsonResponse(result)

def commoditys(request, c_id=None):
    if request.method == 'GET':
        if c_id:
            # 獲取單一商品
            commodity = Commodity.objects.filter(commodity_id=c_id)
            if not commodity:
                result = {'code': 500, 'error': 'System Error try again'}
                return JsonResponse(result)
            commodity = commodity[0]
            result = {'code': 200, 'commodityid': c_id, 'data': {'commodity_id': commodity.commodity_id, 'commodityname': commodity.commodityname, 'category': commodity.category, 'price': commodity.price, 'quantity': commodity.quantity, 'c_content': commodity.c_content, 'c_photo': encode_datetime(commodity.c_photo)}}
            return JsonResponse(result)



def make_commoditys_result(obj):
    result = {'code': 200, 'data': {}}
    data = {}
    commodity_list = []
    for c in obj:
        d = {}
        d['commodity_id'] = c.commodity_id
        d['commodityname'] = c.commodityname
        d['category'] = c.category
        d['price'] = c.price
        d['quantity'] = c.quantity
        d['c_content'] = c.c_content
        # d['c_photo'] = (c.c_photo).path
        d['c_photo'] = encode_datetime(c.c_photo)
        commodity_list.append(d)
    data['commoditys'] = commodity_list
    result['data'] = data
    return result


def encode_datetime(obj):
    """
    Extended encoder function that helps to serialize dates and images
    """
    if isinstance(obj, datetime.date):
        try:
            return obj.strftime('%Y-%m-%d')
        except ValueError as e:
            return ''

    if isinstance(obj, ImageFieldFile):
        try:
            return obj.path
        except ValueError as e:
            return ''

    raise TypeError(repr(obj) + " is not JSON serializable")