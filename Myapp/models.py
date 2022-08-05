from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from django.core.exceptions import ValidationError


# from django.utils.translation import gettext_lazy as _


# Create your models here.
class Topic(models.Model):
    Category_choice = [(1, 'Business'), (2, 'IT & Software'), (3, 'Finance & Accounting'), (4, 'Health&Fitness'),
                       (6, 'Development'), ]
    name = models.CharField(max_length=200)
    category = models.IntegerField(choices=Category_choice)

    def __str__(self):
        index = self.category
        ##一开始跳过了5，所以数据库里存的development都是6，和list的顺序不符合，这里是写死index和list的顺序一致
        ##如果不是按顺序写死，可以每次遍历，获得category相同的元素的第二个属性
        if index == 6:
            index = 5
        return self.name + ' ' + Topic.Category_choice[index - 1][1]


class Student(User):
    CITY_CHOICES = [('WS', 'Windsor'), ('CG', 'Calgery'), ('MR', 'Montreal'), ('VC', 'Vancouver')]
    School_CHOICES = [('WS', 'Windsor'), ('CG', 'Calgery'), ('MR', 'Montreal'), ('VC', 'Vancouver')]
    school = models.CharField(max_length=50, null=True, blank=True, choices=School_CHOICES, default='WS')
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    interested_in = models.ManyToManyField(Topic)
    #需要安装Pillow
    avatar = models.ImageField(upload_to="avatar/", null=True, blank=True)

    def course_list(self):
        order_list = Order.objects.filter(student=self)
        course_list = []
        for order in order_list:
            course_list.append(order.course)
        return course_list

    course_list.short_description = 'registered course'

    def __str__(self):
        # return self.first_name+' '+self.last_name + self.school
        return self.username


'''
def validate_price2(price):
    if price < Decimal(50.00) or price > Decimal(500.00):
        raise ValidationError(
            _('%(price)s should be between $50 and %500'),
            params={'price': price},
        )
'''


def validate_price(price):
    if price < Decimal(50.00) or price > Decimal(500.00):
        raise ValidationError('Price should be between $50 and %500')
    else:
        return price


class Course(models.Model):
    # on_delete = models.CASCADE if for, it referred object deleted, this object will be deleted either
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_price])
    # hours = models.IntegerField()
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    # add for lab7
    interested = models.PositiveIntegerField(default=0)
    stages = models.PositiveIntegerField(default=3)

    def discount(self):
        return self.price * Decimal(0.9)

    def __str__(self):
        return self.name


class Order(models.Model):
    Status_Choice = [(0, 'Cancelled'), (1, 'Order Confirmed')]
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE, blank=True)
    levels = models.PositiveIntegerField(null=True, blank=True)
    order_status = models.IntegerField(choices=Status_Choice, default=1)
    order_date = models.DateField(null=True, blank=True)
    # add field for store the price of this order
    order_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def total_cost(self):
        prc = Course.objects.get(course=self.course).price
        return prc

    def __str__(self):
        return self.course.name + self.student.school.__str__()
