from django.urls import path

from mgr import customer, medicine, sign_in_out

urlpatterns = [
    # 副路由表
    path('customers/', customer.dispatcher),
    path('orders/', medicine.dispatcher),
    path('signin/', sign_in_out.signin),
    path('signout/', sign_in_out.signout)
]
