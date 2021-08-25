import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from user.models import UserProfile
from commodity.models import Commodity
from tools.login_check import login_check
from .models import ShoppingCart
# Create your views here.

# 購物車查詢、結帳視圖函數
@login_check('GET','POST')
def get_cart(request):
    # 購物車查詢視圖函數
    # 127.0.0.1:8000/v1/shoppingcarts
    if request.method == 'GET':
        # 獲取用戶名
        user = request.user
        carts = ShoppingCart.objects.filter(u_id=user)
        print(carts)
        if not carts:
            result = {'code': 500, 'error': 'No commidity in cart'}
            return JsonResponse(result)

        result = make_carts_result(carts, user)
        return JsonResponse(result)

    # 購物車結帳視圖函數
    # 127.0.0.1:8000/v1/shoppingcarts
    elif request.method == 'POST':
        user = request.user
        # 檢查用戶購物車狀態是否鎖定
        carts = ShoppingCart.objects.filter(u_id=user)
        if not carts:
            result = {'code': 401, 'error': 'The shopping cart is empty'}
            return JsonResponse(result)
        cart = carts[0]
        # 取得購物車狀態
        status = cart.c_status
        # 確認購物車狀態
        if status == 1:
            result = checkout_carts_result(carts, user)
            return JsonResponse(result)
        elif status == 2:
            result = {'code': 401, 'error': 'Please complete payment'}
            return JsonResponse(result)


# 購物車增、刪、改視圖函數
@login_check('POST', 'PUT', 'DELETE')
def carts(request, commodity_id):
    # 商品頁面新增商品進入購物車
    # 127.0.0.1:8000/v1/shoppingcarts/<commodity_id>
    if request.method == 'POST':
        json_str = request.body
        # 獲取用戶名
        user = request.user
        if not json_str:
            result = {'code': 401, 'error': 'Please'}
            return JsonResponse(result)
        json_obj = json.loads(json_str)
        # 確認商品id存在數據庫
        if commodity_id:
            commoditys = Commodity.objects.filter(commodity_id=commodity_id)
            commodity = commoditys[0]
        else:
            result = {'code': 401, 'error': 'No commodity'}
            return JsonResponse(result)
        # 獲取商品數量
        num = json_obj.get('number')
        # 獲取庫存數量
        quantity = commodity.quantity
        # 確認庫存充足
        if int(quantity) < int(num):
            result = {'code': 401, 'error': 'Inventory shortage'}
            return JsonResponse(result)
        # 檢查用戶購物車狀態是否鎖定
        check_carts = ShoppingCart.objects.filter(u_id=user)
        if check_carts:
            check_cart = check_carts[0]
            # 取得購物車狀態
            status = check_cart.c_status
            # 確認購物車狀態
            if status == 2:
                result = {'code': 401, 'error': 'The shopping cart cannot be changed'}
                return JsonResponse(result)
        # 檢查購物車數據庫u_id是否已有商品
        carts = ShoppingCart.objects.filter(u_id=user, c_id=commodity)
        # 用戶尚未有商品放置購物車
        if not carts:
            # 創建購物車數據
            ShoppingCart.objects.create(u_id=user, c_id=commodity, num=num, c_status=1)
            result = {'code': 200}
            return JsonResponse(result)
        cart = carts[0]
        # 用戶已有商品放置於購物車
        result = add_cart_result(cart, num)
        return JsonResponse(result)

    # 購物車頁面更新商品數量
    # 127.0.0.1:8000/v1/shoppingcarts/<commodity_id>
    elif request.method == 'PUT':
        json_str = request.body
        # 獲取用戶名
        user = request.user
        if not json_str:
            result = {'code': 401, 'error': 'Please'}
            return JsonResponse(result)
        json_obj = json.loads(json_str)
        # 確認商品id存在數據庫
        if commodity_id:
            commoditys = Commodity.objects.filter(commodity_id=commodity_id)
            commodity = commoditys[0]
        else:
            result = {'code': 401, 'error': 'No commodity'}
            return JsonResponse(result)
        # 獲取商品數量
        num = json_obj.get('number')
        print(num)
        # 獲取庫存數量
        quantity = commodity.quantity
        print(quantity)
        # 確認庫存充足
        if int(quantity) < int(num):
            result = {'code': 401, 'error': 'Inventory shortage'}
            return JsonResponse(result)
        # 檢查用戶購物車狀態是否鎖定
        check_carts = ShoppingCart.objects.filter(u_id=user)
        if check_carts:
            check_cart = check_carts[0]
            # 取得購物車狀態
            status = check_cart.c_status
            # 確認購物車狀態
            if status == 2:
                result = {'code': 401, 'error': 'The shopping cart cannot be changed'}
                return JsonResponse(result)
        # 檢查購物車數據庫u_id是否已有商品
        carts = ShoppingCart.objects.filter(u_id=user, c_id=commodity)
        # 用戶尚未有商品放置購物車
        if not carts:
            result = {'code': 500, 'error': 'System error try again'}
            return JsonResponse(result)
        cart = carts[0]
        cart.num = int(num)
        cart.save()
        result = {'code': 200}
        return JsonResponse(result)

    # 購物車頁面刪除購物車中商品
    # 127.0.0.1:8000/v1/shoppingcarts/<commodity_id>
    elif request.method == 'DELETE':
        # 獲取用戶名
        user = request.user
        # 確認商品id存在數據庫
        if commodity_id:
            commoditys = Commodity.objects.filter(commodity_id=commodity_id)
            commodity = commoditys[0]
        else:
            result = {'code': 401, 'error': 'No commodity'}
            return JsonResponse(result)
        # 檢查用戶購物車狀態是否鎖定
        check_carts = ShoppingCart.objects.filter(u_id=user)
        if check_carts:
            check_cart = check_carts[0]
            # 取得購物車狀態
            status = check_cart.c_status
            # 確認購物車狀態
            if status == 2:
                result = {'code': 401, 'error': 'The shopping cart cannot be changed'}
                return JsonResponse(result)
        # 檢查購物車數據庫u_id是否已有商品
        carts = ShoppingCart.objects.filter(u_id=user, c_id=commodity)
        # 用戶尚未有商品放置購物車
        if not carts:
            result = {'code': 500, 'error': 'System error try again'}
            return JsonResponse(result)
        cart = carts[0]
        cart.delete()
        result = {'code': 200}
        return JsonResponse(result)


# 查詢購物車返回data
def make_carts_result(carts, user):
    result = {'code': 200, 'data': {}}
    data = {}
    cart_list = []
    for c in carts:
        d = {}
        d['cart_id'] = c.car_id
        d['uid'] = user.username
        # 從外鍵->商品id獲取購物車內每筆商品名稱、單價
        c_names = Commodity.objects.filter(commodity_id=c.c_id.commodity_id)
        c_name = c_names[0]
        d['commodity_id'] = c_name.commodity_id
        d['c_name'] = c_name.commodityname
        d['c_price'] = c_name.price
        d['num'] = c.num
        d['status'] = c.c_status
        cart_list.append(d)
    data['carts'] = cart_list
    result['data'] = data
    return result

# 購物車增加商品數量處理
def add_cart_result(cart, num):
    result = {'code': 200}
    cart.num = int(cart.num) + int(num)
    cart.save()
    return result

# 購物車結帳狀態修改，商品模塊數量修改
def checkout_carts_result(carts, user):
    result = {'code': 200, 'data': {}}
    data = {}
    cart_list = []
    for c in carts:
        d = {}
        d['cart_id'] = c.car_id
        d['uid'] = user.username
        # 從外鍵->商品id獲取購物車內每筆商品名稱、單價
        c_names = Commodity.objects.filter(commodity_id=c.c_id.commodity_id)
        c_name = c_names[0]
        d['c_name'] = c_name.commodityname
        d['c_price'] = c_name.price
        d['num'] = c.num
        # 更新商品數據
        c_name.quantity = c_name.quantity - c.num
        c_name.save()
        # 更新購物車狀態
        c.c_status = 2
        c.save()
        d['status'] = c.c_status
        cart_list.append(d)
    data['carts'] = cart_list
    result['data'] = data
    return result

