from django.urls import path, include

from . import views

app_name = 'djangoroku_app'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'send/', views.send_msg, name='send_msg'),
    ]
