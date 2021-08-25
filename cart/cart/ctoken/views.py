import hashlib
import json
import time

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from user.models import UserProfile

def tokens(request):
    '''
    創建token == 登錄
    :param request:
    :return:
    '''
    if not request.method == 'POST':
        result = {'code': 400, 'error': 'Please use POST'}
        return JsonResponse(result)
    # 前端地址
    # 獲取前端傳來的數據/生成token
    # 獲取-校驗密碼-生成token
    # 獲取前端提交的數據
    json_str = request.body
    if not json_str:
        result = {'code': 400, 'error': 'Please send json'}
        return JsonResponse(result)
    json_obj = json.loads(json_str)
    username = json_obj.get('username')
    if not username:
        result = {'code': 400, 'error': 'Please send username'}
        return JsonResponse(result)
    password = json_obj.get('password')
    if not password:
        result = {'code': 400, 'error': 'Please send password'}
        return JsonResponse(result)
    # 驗證登錄使用者資料
    user = UserProfile.objects.filter(username=username)
    if not user:
        result = {'code': 400, 'error': 'username or password is wrong'}
        return JsonResponse(result)
    user = user[0]
    m = hashlib.md5()
    m.update(password.encode()+username.encode())
    if m.hexdigest() != user.password:
        result = {'code': 400, 'error': 'username or password is wrong'}
        return JsonResponse(result)
    # make token
    token = make_token(username)
    result = {'code': 200, 'username': username, 'data': {'token': token.decode()}}
    return JsonResponse(result)


def make_token(username, expire=3600*24):
    # 官方jwt / 自定義jwt
    import jwt
    key = '123456789'
    now = time.time()
    payload = {'username': username, 'exp': int(now + expire)}
    return jwt.encode(payload, key, algorithm='HS256')



