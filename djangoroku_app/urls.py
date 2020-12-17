print(__file__)
from django.urls import path, include

from . import views

app_name = 'djangoroku_app'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'write/', views.write, name='write'),
    ]
