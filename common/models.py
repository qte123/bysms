import datetime

from django.db import models


class Customer(models.Model):
    # 这是用sqlite建表
    # 客户
    name = models.CharField(max_length=200)

    # 联系电话
    phonenumber = models.CharField(max_length=200)

    # 地址
    address = models.CharField(max_length=200)


class Medicine(models.Model):
    # 药物名
    name = models.CharField(max_length=200)
    # 药物编号
    sn = models.CharField(max_length=200)
    # 描述
    desc = models.CharField(max_length=200)


class Order(models.Model):
    # 订单名
    name = models.CharField(max_length=200, null=True, blank=True)
    # 创建日期
    create_date = models.DateTimeField(default=datetime.datetime.now)
    # 客户
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)  # CASCADE 删除主键记录和相应的外键记录 PROTECT 禁止删除记录
    # 订单购买的药品，和Medicine表是多对多的关系
    medicines = models.ManyToManyField(Medicine, through='OrderMedicine')


class OrderMedicine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)

    # 订单中药品的数量
    amount = models.PositiveIntegerField()


from django.contrib import admin

admin.site.register(Customer)


# 国家表
class Country(models.Model):
    name = models.CharField(max_length=100)


# 学生表 country 字段是国家的外键，形成一对多的关系
class Student(models.Model):
    name = models.CharField(max_length=200)
    grade = models.PositiveSmallIntegerField()
    # 等于student里的有个country对象
    country = models.ForeignKey(Country,
                                on_delete=models.PROTECT,
                                # 指定反向访问名字
                                related_name='students')
