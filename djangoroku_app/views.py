print(__file__)
from contextlib import suppress
from typing import Optional

from django.db.models import QuerySet

from django.contrib import messages
import json

from django.shortcuts import HttpResponse, redirect

import logger
from djangoroku_app import models
from djangoroku_app.error import ReceiverDoesNotExist, SenderDoesNotExist

log = logger.getLogger()


def _error(request, error: str) -> None:
    messages.error(request, error)
    log.error(error, stacklevel=2)


def _respond_warning(request, warning: str):
    messages.warning(request, warning)
    log.warning(warning, stacklevel=2)
    return HttpResponse(warning.encode(errors='replace'))


def _respond_success(request, success: str):
    messages.success(request, success)
    log.info(success, stacklevel=2)
    return HttpResponse(success.encode(errors='replace'))


def _respond_error_and_redirect(request, error: str, redirecturl='/'):
    _error(request, error)
    return redirect(redirecturl)


def _bad_read(request):
    error = "\n".join((f"'/read' endpoint must be of either the following forms:",
                       f"/read/user/USERNAME[/filter or multifilter]",
                       f"/read/msg/MSG_ID",
                       f"Instead, you tried to access '{request.path}'",
                       "Redirecting..."))
    return _respond_error_and_redirect(request, error)


def _bad_delete(request):
    error = "\n".join((f"'/delete' endpoint must be of either the following forms:",
                       f"/delete/MSG_ID",
                       f"Instead, you tried to access '{request.path}'",
                       "Redirecting..."))
    return _respond_error_and_redirect(request, error)


def _parse_queryfilter(request, queryfilter: str = None) -> dict:
    """Translates 'read=false', or '(read=false AND receiver=daniel)'
     to {'read':False} or {'read':False, 'receiver':'daniel'} respectively
     """
    if not queryfilter:
        return {}
    if 'OR' in queryfilter:
        _error(request, f"Got a complex filter with OR: {queryfilter}. Not yet implemented.")
        return {}
    
    def _parse_one_pair(_query: str) -> dict:
        """Translates 'read=false' to {'read':False}"""
        _prop, _, _val = map(str.strip, _query.strip().partition('='))
        with suppress(AttributeError):
            # AttributeError is raised when _val is bool, which is what we want in the first place
            if _val.lower() == 'false':
                _val = False
        
        with suppress(AttributeError):
            if _val.lower() == 'true':
                _val = True
        return {_prop: _val}
    
    if 'AND' in queryfilter:
        pairs = queryfilter.split('AND')
        filters = {}
        for pair in map(str.strip, pairs):
            filters.update(_parse_one_pair(pair))
        return filters
    return _parse_one_pair(queryfilter)


def _get_person_by_username(request, username) -> Optional[models.Person]:
    try:
        user: models.Person = models.Person.objects.get_by_natural_key(username)
        return user
    except models.Person.DoesNotExist as e:
        _error(request, f"User with user name: '{username}' does not exist")
        return None
    except Exception as e:
        _error(request, f"{e.__class__.__qualname__} when trying to get person by username: '{username}': {', '.join(map(repr, e.args))}")
        return None


def _get_msg_by_id(request, msg_id: str) -> Optional[models.Message]:
    try:
        msg: models.Message = models.Message.objects.get(id=msg_id)
    except models.Message.DoesNotExist as e:
        _error(request, f"Message with id: '{msg_id}' does not exist")
        return None
    except Exception as e:
        _error(request, f"{e.__class__.__qualname__} when trying to get message by id: '{msg_id}': {', '.join(map(repr, e.args))}")
        return None
    return msg


def index(request, *args, **kwargs):
    return HttpResponse()


def write(request, *args, **kwargs):
    log.debug(f'write({request = }, {args = }, {kwargs = })')
    data = json.loads(request.body.decode())
    log.info(f'{data = }')
    
    try:
        msg = models.Message(**data)
    except SenderDoesNotExist as se:
        return _respond_error_and_redirect(request, f"Sender with user name: '{se.username}' does not exist")
    except ReceiverDoesNotExist as re:
        return _respond_error_and_redirect(request, f"Receiver with user name: '{re.username}' does not exist")
    
    msg.save()
    return _respond_success(request, f"saved Message to db: {msg}")


def read_user_msg(request, username: str, queryfilter: str = None) -> HttpResponse:
    user = _get_person_by_username(request, username)
    if user is None:
        return redirect('/')
    
    log.debug(f'{username = }, {user = }')
    filters: dict = _parse_queryfilter(request, queryfilter)
    log.debug(f'{queryfilter = }, {filters = }')
    if 'receiver' in filters:
        receiver_username = filters.get('receiver')
        receiver = _get_person_by_username(request, receiver_username)
        if receiver is None:
            return _respond_warning(request, (f"Could not find messages where sender = {user} and filters are {filters}, "
                                              f"because receiver '{receiver_username}' does not exist"))
        filters['receiver'] = receiver.id
    user_messages: QuerySet = models.Message.objects.filter(sender=user, **filters)
    if not user_messages:
        warning = f"Could not find messages where sender = {user}"
        if filters:
            warning += f" that match these filters: {filters}"
        return _respond_warning(request, warning)
    update_count = user_messages.update(read=True)
    success = f"Fetched {update_count} Messages where sender = {user}"
    if filters:
        success += f" and filters are: {filters}."
    success += f" All of them are now marked as read=True.\n{user_messages}"
    return _respond_success(request, success)


def read_msg_by_id(request, msg_id: str) -> HttpResponse:
    msg = _get_msg_by_id(request, msg_id)
    if msg is None:
        return redirect('/')
    msg.read = True
    msg.save()
    return _respond_success(request, f"Fetched {msg} with id = {msg_id}. It is now marked as read=True.")


def delete_msg_by_id(request, msg_id: str) -> HttpResponse:
    msg = _get_msg_by_id(request, msg_id)
    if msg is None:
        return redirect('/')
    try:
        delete_count, _ = msg.delete()
    except Exception as e:
        return _respond_error_and_redirect(request, f"{e.__class__.__qualname__} when deleting {msg} with id = {msg_id}")
    return _respond_success(request, f"Deleted {msg} with id = {msg_id}")


def read(request, *args, **kwargs):
    log.debug(f'read({request = }, {args = }, {kwargs = })')
    if not kwargs:
        return _bad_read(request)
    if 'username' in kwargs:
        queryfilter = kwargs.get('filter') or kwargs.get('multifilter')
        return read_user_msg(request, kwargs['username'], queryfilter)
    
    elif 'msg_id' in kwargs:
        return read_msg_by_id(request, kwargs['msg_id'])
    else:
        return _bad_read(request)


def delete(request, *args, **kwargs):
    log.debug(f'delete({request = }, {args = }, {kwargs = })')
    msg_id = kwargs.get('msg_id')
    if not msg_id:
        return _bad_delete(request)
    return delete_msg_by_id(request, kwargs['msg_id'])


def dbg(request, *args, **kwargs):
    breakpoint()
    return HttpResponse()
