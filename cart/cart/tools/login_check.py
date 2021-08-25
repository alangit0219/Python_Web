# login_check('PUT','GET','POST')
import jwt
from django.http import JsonResponse
from user.models import UserProfile

KEY = '123456789'
def login_check(*methods):
    def _login_check(func):
        def wrapper(request, *args, **kwargs):
            # 通過request檢查token
            # 校驗不通過， return JsonResponse()
            # user 查詢出來
            token = request.META.get('HTTP_AUTHORIZATION')
            # 判斷當前請求為('PUT','POST','GET')三種類型
            if request.method not in methods:
                return func(request, *args, **kwargs)
            if not token:
                result = {'code': 401, 'error': 'Please login'}
                return JsonResponse(result)
            try:
                res = jwt.decode(token, KEY, algorithms=['HS256'])
                print(res)
            except jwt.ExpiredSignatureError:
                # token過期
                result = {'code': 403, 'error': 'Please login'}
                return JsonResponse(result)
            except Exception as e:
                result = {'code': 401, 'error': 'Please login'}
                return JsonResponse(result)

            username = res['username']
            try:
                user = UserProfile.objects.get(username=username)
            except:
                user = None
            if not user:
                result = {'code': 401, 'error': 'no user'}
                return JsonResponse(result)
            # 將查詢成功的user賦值給request
            request.user = user
            return func(request, *args, **kwargs)
        return wrapper
    return _login_check

