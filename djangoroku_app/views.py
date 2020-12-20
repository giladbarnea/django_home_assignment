from django.contrib import messages

print('\n', __file__)
import json

from django.shortcuts import HttpResponse, redirect
from rich.console import Console

import logger
from djangoroku_app import models

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


def _bad_read(request):
    error = "\n".join((f"'/read' endpoint must be of either the following forms:",
                       f"/read/user/USERNAME[/filter or multifilter]",
                       f"/read/msg/MSG_ID[/filter or multifilter]",
                       f"Instead, you tried to access '{request.path}'",
                       "Redirecting..."))
    messages.error(request, error)
    log.error(error)
    return redirect('/')


def read(request, *args, **kwargs):
    log.debug(f'read({request = }, {args = }, {kwargs = })')
    if not kwargs:
        return _bad_read(request)
    if 'username' in kwargs:
        username = kwargs['username']
    elif 'msg_id' in kwargs:
        msg_id = kwargs['msg_id']
    else:
        return _bad_read(request)
    return HttpResponse(b"Hello from read")


def dbg(request, *args, **kwargs):
    breakpoint()
    return HttpResponse()
