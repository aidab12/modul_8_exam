from django.db.models import TextChoices, CharField, TextField, ForeignKey, CASCADE

from apps.models.base import UUIDBaseModel, CreatedBaseModel


class Test(CreatedBaseModel):
    title = CharField(max_length=155)
    description = TextField()


class Option(UUIDBaseModel):
    test = ForeignKey('apps.Test', CASCADE, related_name='options')

    class Alphabet(TextChoices):
        A = 'a', 'a'
        b = 'b', 'b'
        C = 'c', 'c'
        D = 'd', 'd'
        F = 'f', 'f'

    alphabet = CharField(
        max_length=1,
        choices=Alphabet.choices,
        default=Alphabet.A)

    description = TextField()