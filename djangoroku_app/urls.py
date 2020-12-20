print(__file__)
from django.urls import path, re_path, include

from . import views

app_name = 'djangoroku_app'

read_user_subpaths = [
    # /read/user (bad)
    path(r'', views.read, name=f'read-user$'),
    # /read/user/john
    path(r'<username>/', views.read, name=f'read-username'),
    
    # /read/user/john/read=false
    re_path(r'(?P<username>\w*)/(?P<filter>[\w=]*)/', views.read, name=f'read-username-filter'),
    
    # /read/user/john/(read=false AND receiver=daniel)
    re_path(r'(?P<username>\w*)/\((?P<multifilter>[\w= ]*)\)/', views.read, name=f'read-username-multifilter')
    ]

read_msg_subpaths = [
    # /read/msg (bad)
    path(r'', views.read, name=f'read-msg$'),
    # /read/msg/42
    path(r'<msg_id>/', views.read, name=f'read-msg'),
    
    ]

read_subpaths = [
    # /read
    path('', views.read, name='read'),
    
    # /read/msg
    path('msg/', include(read_msg_subpaths)),
    # /read/user
    path('user/', include(read_user_subpaths)),
    
    ]

delete_subpaths = [
    # /delete (bad)
    path('', views.delete, name='delete'),
    
    # /delete/42
    path(r'<msg_id>/', views.delete, name=f'delete-msg'),
    
    ]
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'write/', views.write, name='write'),
    
    path(r'read/', include(read_subpaths)),
    path(r'delete/', include(delete_subpaths)),
    path(r'dbg/', views.dbg, name='dbg'),
    ]
