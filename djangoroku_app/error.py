from django.core.exceptions import ObjectDoesNotExist


class PersonDoesNotExist(ObjectDoesNotExist):
    def __init__(self, *args, **kwargs):
        self.username = kwargs.get('username')
        super().__init__(*args)


class ReceiverDoesNotExist(PersonDoesNotExist):
    pass


class SenderDoesNotExist(PersonDoesNotExist):
    pass
