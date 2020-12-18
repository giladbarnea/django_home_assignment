print(__file__)
from django.db import models


# Create your models here.
class Message(models.Model):
    sender = models.CharField(max_length=100, null=False, unique=False)
    receiver = models.CharField(max_length=100, null=False, unique=False)
    message = models.TextField(max_length=256, null=False, unique=False)
    subject = models.CharField(max_length=100, unique=False)
    
    def __init__(self, **kwargs):
        super().__init__()
        self.sender = kwargs['sender']
        self.receiver = kwargs['receiver']
        self.message = kwargs['message']
        self.subject = kwargs['subject']
