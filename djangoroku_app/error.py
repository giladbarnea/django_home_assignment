from django.db import models


class ReceiverDoesNotExist(models.ObjectDoesNotExist):
    
    def __init__(self, *args, sender, receiver, message_id=None) -> None:
        if message_id:
            super().__init__(*args, f"user '{sender} tried to send user '{receiver}' a message (id: '{message_id}'), but user '{receiver}' does not exist")
        else:
            super().__init__(*args, f"user '{sender} tried to send user '{receiver}' a message, but user '{receiver}' does not exist")
