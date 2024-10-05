from mongoengine import DateTimeField, ListField, ReferenceField, StringField, Document
from conf import connect


class Author(Document):
    fullname = StringField(max_length=120, required=True)
    born_date = DateTimeField(required=True)
    born_location = StringField()
    description = StringField()


class Quote(Document):
    quote = StringField(required=True)
    author = ReferenceField(Author)
    tags = ListField(required=True)
