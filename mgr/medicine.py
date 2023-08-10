from common.units.JSONResponse import get_json

# 导入Medicine对象定义
from common.models import Medicine

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
    if action == 'list_customer':
        return list_medicine(request)
    elif action == 'add_customer':
        return addmedicine(request)
    elif action == 'modify_customer':
        return modifymedicine(request)
    elif action == 'del_customer':
        return deletemedicine(request)
    else:
        return get_json({'ret': 1, 'msg': '不支持该类型http请求'})


def list_medicine(request):
    # 返回一个QuerySet 对象，包含所有表记录
    qs = Medicine.objects.values()
    # 将QuerySet对象转化为list字符串
    # 否则不能转化为JSON字符串
    retlist = list(qs)
    return get_json({'ret': 0, 'retlist': retlist})


def addmedicine(request):
    info = request.params['data']
    # 从请求消息中，获取要添加客户的信息
    # 并且插入到数据库中
    medicine = Medicine.objects.create(name=info['name'], sn=info['sn'], desc=info['desc'])
    return get_json({'ret': 0, 'id': medicine.id})


def modifymedicine(request):
    # 从请求消息中，获取修改客户的信息
    # 找到该客户，并且进行修改操作
    medicineid = request.params['id']
    newdata = request.params['newdata']
    try:
        # 根据id从数据库中找到相应的客户记录
        medicine = Medicine.objects.get(id=medicineid)
    except Medicine.DoesNotExist:
        return get_json({
            'ret': 1,
            'msg': f'id为`{medicineid}`的药品不存在'
        })
    if 'name' in newdata:
        medicine.name = newdata['name']
    if 'sn' in newdata:
        medicine.sn = newdata['sn']
    if 'desc' in newdata:
        medicine.desc = newdata['desc']

    # 注意，一定要执行save才能将修改信息保存到数据库里
    medicine.save()
    return get_json({'ret': 0})


def deletemedicine(request):
    medicineid = request.params['id']
    try:
        # 根据id从数据库中找到相应的客户记录
        medicine = Medicine.objects.get(id=medicineid)
    except Medicine.DoesNotExist:
        return get_json({
            'ret': 1,
            'msg': f'id为`{medicineid}`的药品不存在'
        })

    # delete 方法就将该记录从数据库中删除了
    medicine.delete()
    return get_json({'ret': 0})
