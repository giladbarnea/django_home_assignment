from django.urls import path, include

from . import views

app_name = 'djangoroku_app'

urlpatterns = [
    path(r'', views.index, name='index'),
    ]
