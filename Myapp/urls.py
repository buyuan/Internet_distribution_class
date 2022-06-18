#这个是这个'Myapp'的urls

from django.urls import path, include
from Myapp import views

app_name = 'Myapp'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about', views.about, name='about'),
    path(r'detail/<int:top_on>/', views.detail, name='detail'),
]