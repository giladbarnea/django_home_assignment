print(__file__)
import json

from django.shortcuts import HttpResponse
from rich.console import Console

import logger
from . import models

console = Console()
log = logger.getlogger()


# @ensure_csrf_cookie
def index(request, *args, **kwargs):
    print(f'index(args: {args}, kwargs: {kwargs})')
    return HttpResponse(b"Hello from index")


def write(request, *args, **kwargs):
    log.debug(f'write({request = }, {args = }, {kwargs = })')
    data = json.loads(request.body.decode())
    log.info(f'{data = }')
    
    msg = models.Message(**data)
    msg.save()
    log.info(f"saved Message to db: {msg}")
    
    return HttpResponse(b"Hello from write")


def read(request, *args, **kwargs):
    log.debug(f'read({request = }, {args = }, {kwargs = })')
    data = json.loads(request.body.decode())
    log.info(f'{data = }')
    return HttpResponse(b"Hello from read")


def dbg(request, *args, **kwargs):
    breakpoint()
    return HttpResponse()
