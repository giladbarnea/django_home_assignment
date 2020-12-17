print(__file__)
import json

from django.shortcuts import HttpResponse
from rich.pretty import pprint
from rich.console import Console
import rich
import logger
import debug

# pretty.install()

console = Console()
log = logger.getlogger()


# @ensure_csrf_cookie
def index(request, *args, **kwargs):
    print(f'index(args: {args}, kwargs: {kwargs})')
    return HttpResponse(b"Hello from index")


def write(request, *args, **kwargs):
    console.log(f'write({request}, args: {args}, kwargs: {kwargs})')
    
    debug.printattr(request, request.method)
    debug.printattr(request, 'session')
    debug.printattr(request, 'user')
    
    if request.method == 'POST':
        decoded = request.readline().decode()
        if decoded:
            data = json.loads(decoded)
            pprint(data)
    
    return HttpResponse(b"Hello from write")


def dbg(request, *args, **kwargs):
    breakpoint()
    return HttpResponse()
