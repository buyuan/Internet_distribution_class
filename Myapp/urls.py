#这个是这个'Myapp'的urls

from django.urls import path, include
from Myapp import views

app_name = 'Myapp'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about', views.about, name='about'),
    path(r'detail/<int:top_on>/', views.detail, name='detail'),
    path(r'test', views.test, name='test'),
    path(r'courses', views.courses, name='course_list'),
    path(r'place_order', views.place_order, name='place_order'),
    path(r'courses/<int:cour_id>/', views.coursedetail, name='coursedetail'),
    path(r'login', views.user_login, name='login'),
    path(r'logout', views.user_logout, name='logout'),
    path(r'myaccount', views.myaccount, name='myaccount'),
    path(r'testCookie', views.testCookie, name='testCookie'),
]