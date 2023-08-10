from django.db import transaction
from django.db.models import F
from common.units.JSONResponse import get_json
# 导入 Order 对象定义
from common.models import Order, OrderMedicine
import json


def dispatcher(request):
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
    if action == 'list_order':
        return list_order(request)
    elif action == 'add_order':
        return add_order(request)
    # 订单不支持修改和删除
    else:
        return get_json({'ret': 1, 'msg': '不支持该类型http请求'})


def list_order(request):
    # 返回一个QuerySet 对象，包含所有表记录
    # annotate将customer_
    qs = Order.objects.annotate(customer_name=F('customer__name'), medicines_name=F('medicines__name')).values(
        'id', 'name', 'create_date',
        # 两个下划线，表示customer外键关联的表中的name字段的值
        'customer_name', 'medicines_name'
    )
    # 将QuerySet对象转化为list字符串
    # 否则不能转化为JSON字符串
    retlist = list(qs)

    # 可能有ID相同,药品不同的订单，需要合并
    newlist = []
    id2order = {}
    for one in retlist:
        orderid = one['id']
        if orderid not in id2order:
            newlist.append(one)
            id2order[orderid] = one
        else:
            id2order[orderid]['medicines_name'] += '|' + one['medicines_name']
    return get_json({'ret': 0, 'retlist': newlist})


def add_order(request):
    info = request.params['data']
    # 从请求消息中，获取要添加客户的信息
    # 并且插入到数据库中
    # 开启事务
    with transaction.atomic():
        new_order = Order.objects.create(name=info['name'], customer_id=info['customer_id'])
        batch = [OrderMedicine(order_id=new_order.id, medicine_id=mid, amount=1) for mid in info['medicineid']]
        OrderMedicine.objects.bulk_create(batch)
    return get_json({'ret': 0, 'id': new_order.id})
