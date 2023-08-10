from django.urls import path

from sales.views import listorders, listcustomers

urlpatterns = [
    # 副路由表
    path('orders/', listorders),
    path('customers/', listcustomers),
]
