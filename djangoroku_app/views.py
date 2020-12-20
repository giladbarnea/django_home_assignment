from django.http import QueryDict

print(__file__)
import json

from django.shortcuts import HttpResponse
from rich.console import Console

import logger
from djangoroku_app import models
from rich.pretty import pprint

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
    response = f"saved Message to db: {msg}"
    log.info(response)
    
    return HttpResponse(response.encode(errors='replace'))


def read(request, *args, **kwargs):
    log.debug(f'read({request = }, {args = }, {kwargs = })')
    # from rich.pretty import print
    qdict: QueryDict = request.GET
    pprint(qdict, console=console)
    return HttpResponse(b"Hello from read")


def dbg(request, *args, **kwargs):
    breakpoint()
    return HttpResponse()
