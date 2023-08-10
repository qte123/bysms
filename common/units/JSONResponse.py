# JSON工具文件
from django.http import JsonResponse


# 解决json中文乱码
def get_json(json):
    return JsonResponse(json, json_dumps_params={'ensure_ascii': False})
