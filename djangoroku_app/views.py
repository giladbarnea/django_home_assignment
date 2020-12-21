print(__file__)
import json
from contextlib import suppress
from typing import Tuple, overload

from django.contrib import messages
from django.db.models import QuerySet
from django.http import HttpResponseServerError, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import HttpResponse

import logger
from djangoroku_app import models
from djangoroku_app.error import ReceiverDoesNotExist, SenderDoesNotExist

log = logger.getLogger()


def _error(request, error: str) -> None:
    messages.error(request, error)
    log.error(error, stacklevel=3)


########################
### Response methods ###
# Output to contrib.messages and log
########################
def _respond_warning(request, warning: str) -> HttpResponse:
    messages.warning(request, warning)
    log.warning(warning, stacklevel=2)
    return HttpResponse(warning.encode(errors='replace'))


def _respond_success(request, success: str) -> HttpResponse:
    messages.success(request, success)
    log.info(success, stacklevel=2)
    return HttpResponse(success.encode(errors='replace'))


def _server_error(request, error: str) -> HttpResponseServerError:
    _error(request, error)
    return HttpResponseServerError(error.encode(errors='replace'))


def _not_found(request, error: str) -> HttpResponseNotFound:
    _error(request, error)
    return HttpResponseNotFound(error.encode(errors='replace'))


####################
### Bad requests ###
# Explain each endpoint's corrent usage (read, write, delete)
####################
def _bad_read(request):
    error = "\n".join((f"'/read' endpoint must be of either the following forms:",
                       f"/read/user/<username>[/<filter or multifilter>]",
                       f"/read/msg/<msg_id>",
                       f"Instead, you tried to access '{request.path}'"))
    _error(request, error)
    return HttpResponseBadRequest(error.encode(errors='replace'))


def _bad_write(request, extra=None):
    if not extra:
        extra = f"This is the request's body: {request.body}"
    
    error = "\n".join((f"'/write' endpoint expects a JSON body with all of the following fields:",
                       f"\tsender: <username>",
                       f"\treceiver: <username>",
                       f"\tmessage: str",
                       f"\tsubject: str",
                       extra)
                      )
    _error(request, error)
    return HttpResponseBadRequest(error.encode(errors='replace'))


def _bad_delete(request):
    error = "\n".join((f"'/delete' endpoint must be of the following form:",
                       f"/delete/<msg_id>",
                       f"Instead, you tried to access '{request.path}'"))
    _error(request, error)
    return HttpResponseBadRequest(error.encode(errors='replace'))


###############
### Helpers ###
###############
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


@overload
def _get_msg_by_id(request, username) -> Tuple[models.Message, bool]:
    ...


@overload
def _get_msg_by_id(request, username) -> Tuple[None, HttpResponse]:
    ...


def _get_msg_by_id(request, msg_id: str):
    """If msg_id is valid, returns a (Message, True) tuple. If failed getting a Message,
    returns a (None, HttpResponse) tuple. In that case the response object has an informative content and type of the problem."""
    try:
        msg: models.Message = models.Message.objects.get(id=msg_id)
        return msg, True
    except models.Message.DoesNotExist as e:
        return None, _not_found(request, f"Message with id: '{msg_id}' does not exist")
    except Exception as e:
        return None, _server_error(request, f"{e.__class__.__qualname__} when trying to get message by id: '{msg_id}': {', '.join(map(repr, e.args))}")


#############
### Views ###
#############
def index(request, *args, **kwargs):
    return HttpResponse()


def read(request, *args, **kwargs):
    """'/read/<mode>/...'
    Works with URL params, not Ajax calls. Run './dev/read.py -h' for instructions."""
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


def read_user_msg(request, username: str, queryfilter: str = None) -> HttpResponse:
    """'/read/user/<username>[/<filter or multifilter>]'"""
    try:
        user: models.Person = models.Person.objects.get_by_natural_key(username)
    except models.Person.DoesNotExist as e:
        return _not_found(request, f"Sender with user name: '{username}' does not exist")
    except Exception as e:
        return _server_error(request, f"{e.__class__.__qualname__} when trying to get Sender by username: '{username}': {', '.join(map(repr, e.args))}")
    
    log.debug(f'{username = }, {user = }')
    filters: dict = _parse_queryfilter(request, queryfilter)
    log.debug(f'{queryfilter = }, {filters = }')
    
    if 'receiver' in filters:
        receiver_username = filters.get('receiver')
        try:
            receiver: models.Person = models.Person.objects.get_by_natural_key(receiver_username)
        except models.Person.DoesNotExist as e:
            return _not_found(request, (f"Could not find messages where sender = {user} and filters are {filters}, "
                                        f"because receiver '{receiver_username}' does not exist"))
        except Exception as e:
            return _server_error(request, f"{e.__class__.__qualname__} when trying to get Receiver by username: '{username}': {', '.join(map(repr, e.args))}")
        filters['receiver'] = receiver.id
    
    user_messages: QuerySet = models.Message.objects.filter(sender=user, **filters)
    if not user_messages:
        error = f"Could not find messages where sender = {user}"
        if filters:
            error += f" that match these filters: {filters}"
        return _not_found(request, error)
    update_count = user_messages.update(read=True)
    success = f"Fetched {update_count} Messages where sender = {user}"
    if filters:
        success += f" and filters are: {filters}."
    success += f"\nAll of them are now marked as read=True.\n{user_messages}"
    return _respond_success(request, success)


def read_msg_by_id(request, msg_id: str) -> HttpResponse:
    """'/read/msg/<msg_id>'"""
    msg, res = _get_msg_by_id(request, msg_id)
    if msg is None:
        return res
    msg.read = True
    msg.save()
    return _respond_success(request, f"Fetched {msg} with id = {msg_id}. It is now marked as read=True.")


def delete_msg_by_id(request, msg_id: str) -> HttpResponse:
    msg, res = _get_msg_by_id(request, msg_id)
    if msg is None:
        return res
    try:
        delete_count, _ = msg.delete()
    except Exception as e:
        return _server_error(request, f"{e.__class__.__qualname__} when deleting {msg} with id = {msg_id}")
    return _respond_success(request, f"Deleted {msg} with id = {msg_id}")


def delete(request, *args, **kwargs):
    """'/delete/<msg_id>'.
    Expects an Ajax call, not URL params. Run './dev/delete.py -h' for instructions."""
    log.debug(f'delete({request = }, {args = }, {kwargs = })')
    msg_id = kwargs.get('msg_id')
    if not msg_id:
        return _bad_delete(request)
    return delete_msg_by_id(request, kwargs['msg_id'])


def write(request, *args, **kwargs) -> HttpResponse:
    """Expects an Ajax call, not URL params. Run './dev/write.py -h' for instructions."""
    log.debug(f'write({request = }, {args = }, {kwargs = })')
    try:
        data = json.loads(request.body.decode(errors='replace'))
    except Exception as e:
        return _bad_write(request)
    
    log.info(f'{data = }')
    
    if any(field not in data for field in models.Message.REQUIRED_FIELDS):
        missing_fields = set(models.Message.REQUIRED_FIELDS) - set(data.keys())
        extra = f"This request was missing: {missing_fields}"
        return _bad_write(request, extra)
    
    try:
        msg = models.Message(**data)
    except SenderDoesNotExist as se:
        return _not_found(request, f"Sender with user name: '{se.username}' does not exist")
    except ReceiverDoesNotExist as re:
        return _not_found(request, f"Receiver with user name: '{re.username}' does not exist")
    except Exception as e:
        return _server_error(request, "\n".join((f"{e.__class__.__qualname__} when trying to create a message with data: {data}",
                                                 f"Exception args: {', '.join(map(repr, e.args))}")))
    
    msg.save()
    return _respond_success(request, f"saved Message to db: {msg}")


def dbg(request, *args, **kwargs):
    breakpoint()
    return HttpResponse()
