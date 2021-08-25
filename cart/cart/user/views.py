import hashlib
import json
import time
import logging
import re

from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from ctoken.views import make_token
from tools.login_check import login_check

# Create your views here.
@login_check('PUT')
def users(request, username=None):

    if request.method == 'GET':
        # print(username)
        # logging.warning('And this, too')
        if username:
            # logging.warning('This message should go to the log file')
            user = UserProfile.objects.filter(username=username)
            if not user:
                result = {'code': 401, 'error': 'User is not exist!'}
                return JsonResponse(result)
            user = user[0]
            # 獲取用戶資料
            result = {'code': 200, 'username': username, 'data': {'username': user.username, 'email': user.email, 'phone': user.phone,'address':user.address}}
            return JsonResponse(result)


    elif request.method == 'POST':
        # request.POST 只能拿表單post提交的數據
        # 創建用戶
        json_str = request.body
        if not json_str:
            result = {'code': 400, 'error': 'Please enter data'}
            return JsonResponse(result)
        json_obj = json.loads(json_str)
        username = json_obj.get('username')
        if not username:
            result = {'code': 400, 'error': 'Pleas enter username'}
            return JsonResponse(result)
        if not username.isalnum():
            result = {'code': 400, 'error': 'Please enter english or number'}
            return JsonResponse(result)
        usertest = re.match('[A-Za-z0-9]{8,16}$',username)
        if not usertest:
            result = {'code': 400, 'error': 'The username is less than 8'}
            return JsonResponse(result)
        email = json_obj.get('email')
        if not email:
            result = {'code': 400, 'error': 'Please enter email'}
            return JsonResponse(result)
        mailtest = re.match(r'[\w.-]+@[^@\s]+\.[a-zA-Z]{2,10}$',email)
        if not mailtest:
            result = {'code': 400, 'error': 'Please enter correct email'}
            return JsonResponse(result)
        password = json_obj.get('password')
        if not password:
            result = {'code': 400, 'error': 'Please enter password'}
            return JsonResponse(result)
        if not password.isalnum():
            result = {'code': 400, 'error': 'Please enter english or number'}
            return JsonResponse(result)
        passwordtest = re.match('[A-Za-z0-9]{8,16}$',password)
        if not passwordtest:
            result = {'code': 400, 'error': 'The password is less than 8'}
            return JsonResponse(result)

        # 優先查詢當前用戶名是否存在
        old_user = UserProfile.objects.filter(username=username)
        if old_user:
            result = {'code': 400, 'error': 'That username is taken , try another'}
            return JsonResponse(result)
        # 密碼處理 md5哈西/散列
        m = hashlib.md5()
        m.update(password.encode()+username.encode())
        phone = address = ''
        try:
            UserProfile.objects.create(username=username,password=m.hexdigest(),email=email,phone=phone,address=address)
        except Exception as e:
            result = {'code': 500, 'error': 'Server is busy , please try again'}
            return JsonResponse(result)
        # make token
        token = make_token(username)
        result = {'code': 200, 'username': username, 'data': {'token':token.decode()}}
        return JsonResponse(result)


    elif request.method == 'PUT':

        request.META.get('HTTP_AUTHORIZATION')
        print(request.META.get('HTTP_AUTHORIZATION'))
        user = request.user
        print(user)
        json_str = request.body
        print(json_str)
        if not json_str:
            result = {'code': 400, 'error': 'Please send json'}
            return JsonResponse(result)
        json_obj = json.loads(json_str)
        if 'email' not in json_obj:
            result = {'code': 400, 'error': 'Please enter email'}
            return JsonResponse(result)
        if 'phone' not in json_obj:
            result = {'code': 400, 'error': 'Please enter phone'}
            return JsonResponse(result)
        if 'address' not in json_obj:
            result = {'code': 400, 'error': 'Please enter address'}
            return JsonResponse(result)
        if 'username' not in json_obj:
            result = {'code': 400, 'error': 'Please enter username'}
            return JsonResponse(result)
        email = json_obj.get('email', '')
        phone = json_obj.get('phone', '')
        address = json_obj.get('address', '')
        username = json_obj.get('username', '')
        if not phone.isdecimal():
            result = {'code': 400, 'error': 'Please enter number only'}
            return JsonResponse(result)
        phone_test = re.match(r'09\d{8}', phone)
        if not phone_test:
            result = {'code': 400, 'error': 'Please enter correct number'}
            return JsonResponse(result)
        request.user.email = email
        request.user.phone = phone
        request.user.address = address
        request.user.username = username
        # # 密碼哈西處理
        # m = hashlib.md5()
        # m.update(password.encode()+user.username.encode())
        # password = m.hexdigest()
        # request.user.password = password
        request.user.save()
        result ={'code': 200, 'username': request.user.username}
        return JsonResponse(result)


    else:
        raise

    return JsonResponse({'code': 500})

