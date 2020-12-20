"""django_home_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

print(__file__)
from django.contrib import admin
from django.urls import path, include
import logger
import sys

logger.init()

import os

IPDB = eval(os.environ.get('DJANGO_HOME_TASK_IPDB', 'True'))
if IPDB:  # manage.py --no-ipdb sets this to False
    import ipdb
    
    sys.breakpointhook = ipdb.set_trace
log = logger.getLogger()
log.debug(f'{IPDB = }')
urlpatterns = [
    path(r'', include('djangoroku_app.urls')),
    path('admin/', admin.site.urls),
    ]
