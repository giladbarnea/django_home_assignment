print(__file__)
from django.urls import path, re_path, include

from . import views

app_name = 'djangoroku_app'

read_user_subpaths = [
    # /read/user (bad)
    path(r'', views.read, name=f'read-user$'),
    # /read/user/morki
    path(r'<username>/', views.read, name=f'read-username'),
    
    # /read/user/morki/read=false
    re_path(r'(?P<username>\w*)/(?P<filter>[\w=]*)/', views.read, name=f'read-username-filter'),
    
    # /read/user/morki/(read=false AND created<TIMESTAMP)
    re_path(r'(?P<username>\w*)/\((?P<multifilter>[\w= ]*)\)/', views.read, name=f'read-username-multifilter')
    ]

read_msg_subpaths = [
    # /read/msg (bad)
    path(r'', views.read, name=f'read-msg$'),
    # /read/msg/42
    path(r'<msg_id>/', views.read, name=f'read-msg'),
    
    # # /read/msg/created<TIMESTAMP
    # re_path(r'(?P<msg_id>\w*)/(?P<filter>[\w=]*)/', views.read, name=f'read-msg-filter'),
    #
    # # /read/msg/(created<TIMESTAMP OR sender=catta)
    # re_path(r'(?P<msg_id>\w*)/\((?P<multifilter>[\w= ]*)\)/', views.read, name=f'read-msg-multifilter')
    ]

read_subpaths = [
    # /read
    path('', views.read, name='read'),
    
    path('msg/', include(read_msg_subpaths)),
    # /read/user
    path('user/', include(read_user_subpaths)),
    
    # *read_user_subpaths
    ]
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'write/', views.write, name='write'),
    # re_path(r'read/user/', include(user_subpaths)),
    # re_path(r'read/user/(?P<username>.+)\?filter:(?P<filter>.+)', views.read),
    path(r'read/', include(read_subpaths)),
    path(r'dbg/', views.dbg, name='dbg'),
    ]
