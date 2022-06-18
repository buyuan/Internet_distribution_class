from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Topic(models.Model):
    Category_choice = [(6, 'Development'), (1, 'Business'), (2, 'IT & Software'), (3, 'Finance & Accounting'), (4, 'Health&Fitness')]
    name = models.CharField(max_length=200)
    category = models.IntegerField(choices=Category_choice)

    def __str__(self):
        return self.name+self.category.__str__()

class Student(User):
    CITY_CHOICES = [('WS', 'Windsor'), ('CG', 'Calgery'), ('MR', 'Montreal'), ('VC', 'Vancouver')]
    School_CHOICES = [('WS', 'Windsor'), ('CG', 'Calgery'), ('MR', 'Montreal'), ('VC', 'Vancouver')]
    school = models.CharField(max_length=50, null=True, blank=True, choices=School_CHOICES, default='WS')
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    interested_in = models.ManyToManyField(Topic)

    def __str__(self):
        #return self.first_name+' '+self.last_name + self.school
        return self.username



class Course(models.Model):
    # on_delete = models.CASCADE if for, it referred object deleted, this object will be deleted either
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField( max_digits=10, decimal_places=2)
    #hours = models.IntegerField()
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(max_length=300, null=True, blank=True)


    def __str__(self):
        return self.name

class Order(models.Model):
    Status_Choice = [(0, 'Cancelled'), (1, 'Order Confirmed')]
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    levels = models.PositiveIntegerField(null=True, blank=True)
    order_status = models.IntegerField(choices=Status_Choice, default=1)
    order_date = models.DateField(null=True, blank=True)

    def total_cost(self):
        prc = Course.objects.get(course=self.course).price
        return prc * self.levels

    def __str__(self):
        return self.course.name + self.student.school.__str__()