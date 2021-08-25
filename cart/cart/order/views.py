from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from user.models import UserProfile
from commodity.models import Commodity
from shoppingcart.models import ShoppingCart
from .models import Order
from tools.login_check import login_check
import json
import time
import uuid
# Paypal checkout import
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest
from paypalhttp import HttpError
from paypalcheckoutsdk.orders import OrdersCaptureRequest



# Create your views here.

@login_check('GET', 'POST')
def orders(request):
    # 訂單查詢視圖函數
    if request.method == 'GET':
        user = request.user
        orders = Order.objects.filter(u_id=user).order_by('-create_time')
        if not orders:
            result = {'code': 401, 'error': 'No order'}
            return JsonResponse(result)
        result = check_orders(orders, user)
        return JsonResponse(result)

    # 結帳後->訂單模塊數據庫建立
    elif request.method == 'POST':
        user = request.user
        # json_str = request.body
        # if not json_str:
        #     result = {'code': 401, 'error': 'Please send json'}
        #     return JsonResponse(result)
        # json_obj = json.loads(json_str)
        # 取得用戶在購物車數據庫資料
        carts = ShoppingCart.objects.filter(u_id=user)
        if not carts:
            result = {'code': 401, 'error': 'System error try again'}
            return JsonResponse(result)
        # 檢查地址、電話是否填寫
        check_address = user.address
        check_phone = user.phone
        if check_address == '':
            result = {'code': 404, 'error': 'Check your address'}
            return JsonResponse(result)
        if check_phone == '':
            result = {'code': 404, 'error': 'Check your phone'}
            return JsonResponse(result)
        # 檢查購物車狀態碼是否已進入結帳程序
        cart = carts[0]
        status = cart.c_status
        if status == 1:
            checkout_carts_result(carts, user)
            # 訂單數據庫資料建立
            result = make_orders(carts, user)
            return JsonResponse(result)
        if status == 2:
            orders = Order.objects.filter(u_id=user, o_status=1)
            order = orders[0]
            order_num = order.order_num
            result = {'code': 401, 'error': 'Please complete payment', 'order_num': order_num}
            return JsonResponse(result)


@login_check('GET', 'DELETE')
def order_detail(request, order_num):
    # 訂單詳細頁面內容
    if request.method == 'GET':
        user = request.user
        if order_num:
            orders = Order.objects.filter(order_num=order_num, u_id=user)
        else:
            result = {'code': 401, 'error': 'No order'}
            return JsonResponse(result)
        result = make_order_detail(orders, user)
        return JsonResponse(result)

    # 取消訂單
    elif request.method == 'DELETE':
        user = request.user
        carts = ShoppingCart.objects.filter(u_id=user)
        if not carts:
            result = {'code': 401, 'error': 'System error try again'}
            return JsonResponse(result)
        if order_num:
            orders = Order.objects.filter(order_num=order_num, u_id=user)
        else:
            result = {'code': 401, 'error': 'No order'}
            return JsonResponse(result)
        cancel_order(orders,carts)
        carts.delete()
        result = {'code': 200}
        return JsonResponse(result)


# Paypal checkout
@login_check('POST')
def total_check(request):
    if request.method == 'POST':
        json_obj = json.loads(request.body)
        total = json_obj.get('total')
        order_num = json_obj.get('order_num')
        if not total:
            result = {'code': 401, 'error': 'No total price'}
            return JsonResponse(result)
        if not order_num:
            result = {'code': 401, 'error': 'No order number'}
        print(order_num)
        # Creating Access Token for Sandbox
        client_id = "AS_oEDKMzXkJjEL16108mAYW7-BwZV7or4g2TCmHdMqV57M2zQoccSMjwQenrPBKnsjJal9TLUSN9_pG"
        client_secret = "EFNpAME70wl8w3eqqqjMvaeKIzj4wqP9w2tgo0rIvYCi9t9fcK8wXsYaQndWDYX_ov17rXTKPzqPdlmA"
        # Creating an environment
        environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
        client = PayPalHttpClient(environment)

        # Construct a request object and set desired parameters
        # Here, OrdersCreateRequest() creates a POST request to /v2/checkout/orders
        request = OrdersCreateRequest()

        request.prefer('return=representation')

        request.request_body (
            {
                "intent": "CAPTURE",
                "application_context": {
                    "return_url": "http://127.0.0.1:5000/payment_completed",
                    "cancel_url": "http://127.0.0.1:5000/order/" + order_num
                },
                "purchase_units": [
                    {
                        "amount": {
                            "currency_code": "TWD",
                            "value": total
                        }
                    }
                ]
            }
        )

        try:
            # Call API with your client and get a response for your call
            response = client.execute(request)
            print(response)
            print ('Order With Complete Payload:')
            print ('Status Code:', response.status_code)
            print ('Status:', response.result.status)
            print ('Order ID:', response.result.id)
            print ('Intent:', response.result.intent)
            print ('Links:')
            print(response.result.links[1].href)
            for link in response.result.links:
                print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
                print( 'Total Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,response.result.purchase_units[0].amount.value))
                # If call returns body in response, you can get the deserialized version from the result attribute of the response
                order = response.result
                print (order)
        except IOError as ioe:
            print (ioe)
            if isinstance(ioe, HttpError):
                # Something went wrong server-side
                print (ioe.status_code)
        order_href = ''
        for i in response.result.links:
            if i.rel == 'approve':
                order_href = i.href
        order_id = response.result.id
        print(order_href)
        result = {'code': 200, 'order_href': order_href, 'order_id': order_id}
        return JsonResponse(result)


# Paypal capture 結帳確認步驟
@login_check('POST')
def capture_order_id(request):
    if request.method == 'POST':
        user = request.user
        json_obj = json.loads(request.body)
        order_id = json_obj.get('order_id')
        if not order_id:
            result = {'code': 401, 'error': 'No order_id'}
            return JsonResponse(result)
        # Order_status 訂單狀態 1 更改為 2
        orders = Order.objects.filter(o_status=1, u_id=user)
        carts = ShoppingCart.objects.filter(u_id=user)
        # Creating Access Token for Sandbox
        client_id = "AS_oEDKMzXkJjEL16108mAYW7-BwZV7or4g2TCmHdMqV57M2zQoccSMjwQenrPBKnsjJal9TLUSN9_pG"
        client_secret = "EFNpAME70wl8w3eqqqjMvaeKIzj4wqP9w2tgo0rIvYCi9t9fcK8wXsYaQndWDYX_ov17rXTKPzqPdlmA"
        # Creating an environment
        environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
        client = PayPalHttpClient(environment)
        request = OrdersCaptureRequest(order_id)
        try:
            # Call API with your client and get a response for your call
            response = client.execute(request)

            # If call returns body in response, you can get the deserialized version from the result attribute of the response
            order = response.result.id
        except IOError as ioe:
            if isinstance(ioe, HttpError):
                # Something went wrong server-side
                print(ioe.status_code)
                print(ioe.headers)
                print(ioe)
                result = {'code': 403, 'error': 'Server error try again'}
                return JsonResponse(result)
            else:
                # Something went wrong client side
                print(ioe)
                result = {'code': 403, 'error': ioe}
                return JsonResponse(result)
        completed_order(orders)
        carts.delete()
        result = {'code': 200}
        return JsonResponse(result)


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


# 訂單數據庫資料建立
def make_orders(carts, user):
    # uuid生成
    order_num = uuid.uuid4().hex[:10]
    for c in carts:
        # 獲取訂單商品數量
        c_num = c.num
        # 獲取訂單商品c_id
        commoditys = Commodity.objects.filter(commodity_id=c.c_id.commodity_id)
        commodity = commoditys[0]
        # 建立訂單數據資料 order_num，u_id，c_id，o_num，o_status
        Order.objects.create(order_num=order_num, u_id=user, c_id=commodity, o_num=c_num, o_status=1)
    result = {'code': 200, 'order_num': order_num}
    return result


# 訂單總列表返回
def check_orders(orders, user):
    result = {'code': 200, 'data': {}}
    data = {}
    # 訂單編號列表
    order_list = []
    # 計算共有幾組訂單編號
    count = 0
    # 紀錄重複訂單編號
    old_number = ['00000000']
    # 訂單編號、建立日期、訂單狀態
    for item in orders:
        order_number = item.order_num
        create_time = item.create_time.strftime('%Y-%m-%d')
        o_status = item.o_status
        count += 1
        if order_number not in old_number:
            d = {}
            # 訂單編號導入
            d['order_num'] = order_number
            # 建立日期導入
            d['create_time'] = create_time
            # 訂單狀態導入
            d['o_status'] = o_status
            # 預設商品數量為0
            d['o_num'] = 0
            order_list.append(d)
            old_number.append(order_number)

    # 依照訂單編號匹配商品總數量
    for o in orders:
        order_num = o.order_num
        o_num = o.o_num
        for i in order_list:
            if order_num == i['order_num']:
                i['o_num'] += o_num
    data['orders'] = order_list
    result['data'] = data
    return result


# 訂單詳細頁面返回
def make_order_detail(orders, user):
    result = {'code': 200, 'data': {}}
    data = {}
    # 訂單編號列表
    order_list = []
    for item in orders:
        d = {}
        # 獲取訂單商品數量
        o_num = item.o_num
        # 獲取訂單建立日期
        create_time = item.create_time.strftime('%Y-%m-%d')
        # 透過獲取訂單c_id，取得商品名稱，商品單價
        commodity_id = item.c_id.commodity_id
        c_names = Commodity.objects.filter(commodity_id=commodity_id)
        c_name = c_names[0]
        d['c_name'] = c_name.commodityname
        d['c_price'] = c_name.price
        d['o_num'] = o_num
        d['create_time'] = create_time
        d['o_status'] = item.o_status
        d['total'] = int(c_name.price) * int(o_num)
        order_list.append(d)
    data['orders'] = order_list
    result['data'] = data
    return result

# 更改訂單狀態碼 3 --> 取消訂單
def cancel_order(orders,carts):
    # 更改訂單狀態碼
    for i in orders:
        i.o_status = 3
        i.save()
    # 商品庫存數量校正
    for c in carts:
        commoditys = Commodity.objects.filter(commodity_id=c.c_id.commodity_id)
        commodity = commoditys[0]
        # 更新商品數據
        commodity.quantity = commodity.quantity + c.num
        commodity.save()

# 更改訂單狀態碼 2 --> 完成訂單
def completed_order(orders):
    # 更改訂單狀態碼
    for i in orders:
        i.o_status = 2
        i.save()

