print(__file__)
from django.db import models
from logger import getlogger
import sys

log = getlogger()


class Message(models.Model):
    sender = models.CharField("The sender's username", max_length=100, null=False, unique=False)
    receiver = models.CharField("The receiver's username", max_length=100, null=False, unique=False)
    message = models.TextField(max_length=256, null=False, unique=False)
    subject = models.CharField(max_length=100, unique=False)
    created = models.DateTimeField(auto_now_add=True)
    REQUIRED_FIELDS = ['sender', 'receiver', 'message', 'subject']  # todo: create dynamically
    
    def __init__(self, *args, **kwargs):
        log.debug(f'{self.__class__.__qualname__}({args = }, {kwargs = })')
        missing_fields = []
        for field in self.REQUIRED_FIELDS:
            if field not in kwargs:
                missing_fields.append(field)
        if missing_fields:
            raise KeyError(f"{self.clsname}() requires the following fields: {', '.join(map(repr, self.REQUIRED_FIELDS))}. "
                           f"The following fields were not provided: {', '.join(map(repr, missing_fields))}")
        # only if all required fields are provided
        super().__init__(*args, **kwargs)
        self.sender = kwargs['sender']
        self.receiver = kwargs['receiver']
        self.message = kwargs['message']
        self.subject = kwargs['subject']
    
    @property
    def clsname(self):
        return self.__class__.__qualname__
    
    def __str__(self):
        """Pretty string displaying the instance's field names and values conveniently"""
        attrs = []
        for attname in [f.attname for f in self._meta.concrete_fields]:
            attval = repr(getattr(self, attname))
            attrs.append(f"{attname}: {attval}")
        attrs_str = "\n\t" + "\n\t".join(attrs)
        return f"{self.clsname}({self.id}){attrs_str}"
