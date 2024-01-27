from mongoengine import Document
from mongoengine.fields import StringField, BooleanField, IntField


class Clients(Document):
    fullname = StringField()
    age = IntField()
    address = StringField()
    email = StringField()
    sended = BooleanField(default=False)