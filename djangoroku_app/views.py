print(__file__)
import json

from django.shortcuts import HttpResponse
from rich.console import Console

# import debug
import logger

# pretty.install()

console = Console()
log = logger.getlogger()


# @ensure_csrf_cookie
def index(request, *args, **kwargs):
    print(f'index(args: {args}, kwargs: {kwargs})')
    return HttpResponse(b"Hello from index")


def write(request, *args, **kwargs):
    log.debug(f'write({request = }, {args = }, {kwargs = })')
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        log.info(f'{data = }')
        from . import models
        msg = models.Message(**data)
        msg.save()
        log.info(f"saved Message to db: {msg}")
    
    return HttpResponse(b"Hello from write")


def dbg(request, *args, **kwargs):
    breakpoint()
    return HttpResponse()
