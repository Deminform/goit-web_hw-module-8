from mongoengine import BooleanField, DateTimeField, ListField, ReferenceField, StringField, Document
from conf.connect import connect


class Subscriber(Document):
    fullname = StringField(max_length=120, required=True)
    email = StringField(max_length=254, required=True)
    email_sent = BooleanField(default=False)
    phone_number = StringField(max_length=20, required=True)
    sms_sent = BooleanField(default=False)
    notify_method = ListField(required=True)
    notify_date = ListField()
