print(__file__)
import json

from django.shortcuts import HttpResponse
from rich.pretty import pprint
from rich.console import Console
from rich import inspect
import rich
import logger

# pretty.install()

console = Console()


# @ensure_csrf_cookie
def index(request, *args, **kwargs):
    print(f'index(args: {args}, kwargs: {kwargs})')
    return HttpResponse(b"Hello from index")


# @csrf_protect
# @ensure_csrf_cookie
def write(request, *args, **kwargs):
    console.log(f'write({request}, args: {args}, kwargs: {kwargs})')
    log = logger.getlogger()
    log.logattr(request, request.method)
    log.logattr(request, 'session')
    log.logattr(request, 'user')
    # inspect(getattr(request, request.method, None), docs=False, title=request.method)
    # inspect(getattr(request, 'session', None), docs=False, title='session')
    # inspect(getattr(request, 'user', None), docs=False, title='user')
    
    if request.method == 'POST':
        decoded = request.readline().decode()
        if decoded:
            data = json.loads(decoded)
            pprint(data)
    
    return HttpResponse(b"Hello from write")
