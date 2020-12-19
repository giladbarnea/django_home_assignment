print(__file__)
from django.urls import path

from . import views

app_name = 'djangoroku_app'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'write/', views.write, name='write'),
    path(r'dbg/', views.dbg, name='dbg'),
    ]
