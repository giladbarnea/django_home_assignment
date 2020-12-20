from typing import List

print(__file__)
from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model
from djangoroku_app.error import ReceiverDoesNotExist
from logger import getlogger

log = getlogger()


class AbstractModel(models.Model):
    class Meta:
        abstract = True
    
    REQUIRED_FIELDS = []
    
    @property
    def clsname(self):
        return self.__class__.__qualname__
    
    def __str__(self):
        """Pretty string displaying the instance's field names and values conveniently"""
        attrs = []
        for attname in [f.attname for f in self._meta.concrete_fields]:
            attval = repr(getattr(self, attname, None))
            if attval == 'None':  # happens when a required field was not provided
                continue
            attrs.append(f"{attname}: {attval}")
        attrs_str = "\n\t" + "\n\t".join(attrs)
        return f"{self.__class__.__qualname__}{attrs_str}"
    
    def _get_missing_fields(self, *provided: str) -> List[str]:
        missing_fields = []
        for field in self.REQUIRED_FIELDS:
            if field not in provided:
                missing_fields.append(field)
        return missing_fields


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='<deleted>')[0]


class Person(User):
    pass
    # username = models.CharField("The sender's username", max_length=100, null=False, unique=False)


class Message(AbstractModel):
    REQUIRED_FIELDS = ['sender', 'receiver', 'message', 'subject']
    # sender = models.CharField("The sender's username", max_length=100, null=False, unique=False)
    sender = models.ForeignKey(Person, on_delete=models.SET(get_sentinel_user), related_name='messages', null=False)
    # receiver = models.CharField("The receiver's username", max_length=100, null=False, unique=False)
    receiver = models.ForeignKey(Person, on_delete=models.SET(get_sentinel_user), null=False)
    message = models.TextField(max_length=256, null=False, unique=False)
    subject = models.CharField(max_length=100, unique=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __init__(self, *args, **kwargs):
        log.debug(f'{self.__class__.__qualname__}({args = }, {kwargs = })')
        
        missing_fields = self._get_missing_fields(*kwargs)
        if missing_fields:
            raise KeyError(f"{self.clsname}() requires the following fields: {', '.join(map(repr, self.REQUIRED_FIELDS))}. "
                           f"The following fields were not provided: {', '.join(map(repr, missing_fields))}")
        
        # Construct only if all required fields are provided
        sender_username = kwargs['sender']
        receiver_username = kwargs['receiver']
        subject = kwargs['subject']
        message = kwargs['message']
        sender = Person.objects.get(username=sender_username)
        receiver = Person.objects.get(username=receiver_username)
        # try:
        #     receiver = User.objects.get(username=receiver_username)
        # except models.ObjectDoesNotExist as doesnt_exist_err:
        #     raise ReceiverDoesNotExist(sender=sender_username, receiver=receiver_username)
        #
        # sender = User.objects.get_or_create(username=sender_username)
        super().__init__(*args, sender=sender, receiver=receiver, subject=subject, message=message)
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.subject = subject
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        # todo: User / sender
