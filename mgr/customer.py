from common.units.JSONResponse import get_json
# 导入 Customer 对象定义
from common.models import Customer
import json


def dispatcher(request):
    print('sssssssss')
    # 根据session判断用户是否能登录的管理员用户
    if 'usertype' not in request.session:
        return get_json({
            'ret': 302,
            'msg': '未登录',
            'redirect': '/mgr/sign.html'
        }, status=302)
    if request.session['usertype'] != 'mgr':
        return get_json({
            'ret': 302,
            'msg': '用户非mgr类型',
            'redirect': '/mgr/sign.html'
        }, status=302)
    # 将请求参数统一放入request的params属性中，方便后续处理

    # GET 请求 参数 在request 对象的GET属性中
    if request.mothod == 'GET':
        request.params = request.GET
    elif request.mothod in ['POST', 'PUT', 'DELETE']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是json格式
        request.params = json.loads(request.body)

    # 根据不同的action分派给不同的函数进行处理
    action = request.params['action']
    if action == 'list_customer':
        return list_customers(request)
    elif action == 'add_customer':
        return addcustomer(request)
    elif action == 'modify_customer':
        return modifycustomer(request)
    elif action == 'del_customer':
        return deletecustomer(request)
    else:
        return get_json({'ret': 1, 'msg': '不支持该类型http请求'})


def list_customers(request):
    # 返回一个QuerySet 对象，包含所有表记录
    qs = Customer.objects.values()
    # 将QuerySet对象转化为list字符串
    # 否则不能转化为JSON字符串
    retlist = list(qs)
    return get_json({'ret': 0, 'retlist': retlist})


def addcustomer(request):
    info = request.params['data']
    # 从请求消息中，获取要添加客户的信息
    # 并且插入到数据库中
    record = Customer.objects.create(name=info['name'], phonenumber=info['phonenumber'], address=info['address'])
    return get_json({'ret': 0, 'id': record.id})


def modifycustomer(request):
    # 从请求消息中，获取修改客户的信息
    # 找到该客户，并且进行修改操作
    customerid = request.params['id']
    newdata = request.params['newdata']
    try:
        # 根据id从数据库中找到相应的客户记录
        customer = Customer.objects.get(id=customerid)
    except Customer.DoesNotExist:
        return get_json({
            'ret': 1,
            'msg': f'id为`{customerid}`的客户不存在'
        })
    if 'name' in newdata:
        customer.name = newdata['name']
    if 'phonenumber' in newdata:
        customer.phonenumber = newdata['phonenumber']
    if 'address' in newdata:
        customer.address = newdata['address']

    # 注意，一定要执行save才能将修改信息保存到数据库里
    customer.save()
    return get_json({'ret': 0})


def deletecustomer(request):
    customerid = request.params['id']
    try:
        # 根据id从数据库中找到相应的客户记录
        customer = Customer.objects.get(id=customerid)
    except Customer.DoesNotExist:
        return get_json({
            'ret': 1,
            'msg': f'id为`{customerid}`的客户不存在'
        })

    # delete 方法就将该记录从数据库中删除了
    customer.delete()
    return get_json({'ret': 0})
