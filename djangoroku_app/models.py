print(__file__)
from django.db import models
from logger import getlogger
from time import time as unixtime

log = getlogger()


# {attr:getattr(self, attr) for attr in [f.attname for f in self._meta.concrete_fields]}
class Message(models.Model):
    sender = models.CharField("The sender's username", max_length=100, null=False, unique=False)
    receiver = models.CharField("The receiver's username", max_length=100, null=False, unique=False)
    message = models.TextField(max_length=256, null=False, unique=False)
    subject = models.CharField(max_length=100, unique=False)
    created: int
    
    def __init__(self, *args, **kwargs):
        epoch = int(unixtime())
        log.debug(f'{self.__class__.__qualname__}({args = }, {kwargs = })')
        super().__init__(*args, **kwargs)
        self.sender = kwargs.get('sender')
        self.receiver = kwargs.get('receiver')
        self.message = kwargs.get('message')
        self.subject = kwargs.get('subject')
        self.created = epoch
    
    def __str__(self):
        attrs = []
        for attname in [f.attname for f in self._meta.concrete_fields]:
            attval = repr(getattr(self, attname))
            attrs.append(f"{attname}: {attval}")
        attrs_str = "\n\t" + "\n\t".join(attrs)
        return f"{self.__class__.__qualname__}({self.id}){attrs_str}"
