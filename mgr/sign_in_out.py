from django.contrib.auth import authenticate, login, logout
from common.units.JSONResponse import get_json


# 登录处理
def signin(request):
    # 从HTTP POST请求中获取用户名、密码参数
    userName = request.POST.get('username')
    passWord = request.POST.get('password')
    print('afafaf')
    # 使用Django auth 库里面的方法校验用户名、密码
    user = authenticate(username=userName, password=passWord)
    # 如果能找到用户，并且密码正确
    if user is not None:
        if user.is_active:
            if user.is_superuser:
                login(request, user)
                # 在session存入用户类型
                request.session['usertype'] = 'mgr'
                request.session['level'] = 9
                return get_json({'ret': 0})
            else:
                return get_json({'ret': 1, 'msg': '请使用管理员账户登录'})
        else:
            return get_json({'ret': 0, 'msg': '用户已经被禁用'})

    # 否则就是用户名、密码错误
    else:
        return get_json({'ret': 1, 'msg': '用户名或密码错误'})


# 登出处理
def signout(request):
    # 使用登出方法
    logout(request)
    return get_json({'ret': 0})
