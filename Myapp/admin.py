from django.contrib import admin
from django.db import models
from .models import Topic, Course, Student, Order
from decimal import Decimal


def upper(obj):
    return obj.name.upper()


class CourseInline(admin.TabularInline):
    model = Course


def discount_10(modeladmin, request, queryset):
    for obj in queryset:
        obj.price = obj.price * Decimal(0.9)
        obj.save()


discount_10.short_description = "Give course 0.1 discount"


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    actions = [discount_10]


class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    inlines = [CourseInline, ]


class OrderAdmin(admin.ModelAdmin):
    list_display = ('course', 'student')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name','course_list', 'email')


admin.site.register(Topic, TopicAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Order, OrderAdmin)

# Register your models here.
