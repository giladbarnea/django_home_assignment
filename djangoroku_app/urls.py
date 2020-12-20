print(__file__)
from django.urls import path, re_path, include

from . import views

app_name = 'djangoroku_app'

user_subpaths = [
    path('', views.read, name='read-user-index'),
    path(r'<username>/', views.read, name=f'read-user-specific'),
    re_path(r'(?P<username>\w*)/(?P<filter>[\w=]*)/', views.read, name=f'read-user-filter'),
    re_path(r'(?P<username>\w*)/\((?P<filter>[\w= ]*)\)/', views.read, name=f'read-user-multifilter')
    ]

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'write/', views.write, name='write'),
    re_path(r'read/user/', include(user_subpaths)),
    # re_path(r'read/user/(?P<username>.+)\?filter:(?P<filter>.+)', views.read),
    path(r'read/', views.read, name='read'),
    path(r'dbg/', views.dbg, name='dbg'),
    ]
