print(__file__)

from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model
from logger import getlogger
from djangoroku_app.error import ReceiverDoesNotExist, SenderDoesNotExist

log = getlogger()


class AbstractModel(models.Model):
    """Model to inherit from that displays props and values nicely"""
    
    class Meta:
        abstract = True
    
    REQUIRED_FIELDS = []
    
    @property
    def clsname(self):
        return self.__class__.__qualname__
    
    def __str__(self):
        attrs = []
        for attname in [f.attname for f in self._meta.concrete_fields]:
            attval = repr(getattr(self, attname, None))
            if attval == 'None':  # happens when a required field was not provided
                continue
            attrs.append(f"{attname}: {attval}")
        attrs_str = "\n\t" + "\n\t".join(attrs)
        return f"{self.__class__.__qualname__}{attrs_str}"


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='<deleted>')[0]


class Person(User, AbstractModel):
    pass


class Message(AbstractModel):
    REQUIRED_FIELDS = ['sender', 'receiver', 'message', 'subject']
    # sender = models.CharField("The sender's username", max_length=100, null=False, unique=False)
    sender = models.ForeignKey(Person, on_delete=models.SET(get_sentinel_user), related_name='messages', null=False)
    # receiver = models.CharField("The receiver's username", max_length=100, null=False, unique=False)
    receiver = models.ForeignKey(Person, on_delete=models.SET(get_sentinel_user), null=False)
    read = models.BooleanField("Whether this message was read (opened) by the receiver", default=False)
    message = models.TextField(max_length=256, null=False, unique=False)
    subject = models.CharField(max_length=100, unique=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __init__(self, *args, **kwargs):
        log.verbose(f'{self.__class__.__qualname__}({args = }, {kwargs = })')
        
        fields = kwargs  # default
        sender_username = kwargs.get('sender')
        if sender_username:
            try:
                sender = Person.objects.get(username=sender_username)
            except Person.DoesNotExist as e:
                raise SenderDoesNotExist(username=sender_username)
            fields['sender'] = sender
        receiver_username = kwargs.get('receiver')
        if receiver_username:
            try:
                receiver = Person.objects.get(username=receiver_username)
            except Person.DoesNotExist as e:
                raise ReceiverDoesNotExist(username=receiver_username)
            fields['receiver'] = receiver
        
        super().__init__(*args, **fields)
