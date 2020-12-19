print(__file__)
from django.db import models
from logger import getlogger

log = getlogger()


# Create your models here.
class Message(models.Model):
    sender = models.CharField("The sender's username", max_length=100, null=False, unique=False)
    receiver = models.CharField("The receiver's username", max_length=100, null=False, unique=False)
    message = models.TextField(max_length=256, null=False, unique=False)
    subject = models.CharField(max_length=100, unique=False)
    
    # created = models.DateTimeField(auto_now_add=True, default=timezone.now())
    
    def __init__(self, *args, **kwargs):
        log.debug(f'Message({args = }, {kwargs = })')
        super().__init__(*args,**kwargs)
        self.sender = kwargs.get('sender')
        self.receiver = kwargs.get('receiver')
        self.message = kwargs.get('message')
        self.subject = kwargs.get('subject')
