import argparse
import json

import connect

from bson.objectid import ObjectId
from mongoengine import DateTimeField, ListField, ReferenceField, StringField, Document


parser = argparse.ArgumentParser(description='Python Web / Homework / Module 8')
parser.add_argument('--action', help='create, update, read, delete, upload')
parser.add_argument('--model', help='author, quote')
parser.add_argument('--id')
parser.add_argument('--fullname')
parser.add_argument('--filepath')
parser.add_argument('--born_date')
parser.add_argument('--born_location')
parser.add_argument('--description')
parser.add_argument('--quote')
parser.add_argument('--author')
parser.add_argument('--tags', nargs='+')

arg = vars(parser.parse_args())
action = arg.get('action')
pk = arg.get('id')
model = arg.get('model')
fullname = arg.get('fullname')
filepath = arg.get('filepath')
born_date = arg.get('born_date')
born_location = arg.get('born_location')
description = arg.get('description')
quote = arg.get('quote')
author = arg.get('author')
tags = arg.get('tags')


class Author(Document):
    fullname = StringField(max_length=120, required=True)
    born_date = DateTimeField(required=True)
    born_location = StringField()
    description = StringField()


class Quote(Document):
    quote = StringField(required=True)
    author = ReferenceField(Author)
    tags = ListField(required=True)


def upload_from_file(filepath, model):
    result = []
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if model == 'author':
        for obj in data:
            result.append((Author(
                fullname=obj['fullname'],
                born_date=obj['born_date'],
                born_location=obj['born_location'],
                description=obj['description'])
                      .save()).to_mongo().to_dict())
    elif model == 'quote':
        for obj in data:
            result.append((Quote(
                quote=obj['quote'],
                author=Author.objects(fullname=obj['author']).first(),
                tags=obj['tags'])
                      .save()).to_mongo().to_dict())
    return result


def find(model):
    result = Author.objects.all() if model == 'author' else Author.objects.all()
    return result


def create(model, fullname='', born_date='', born_location='', description='', quote='', author='', tags=''):
    if model == 'author':
        result = Author(fullname=fullname, born_date=born_date, born_location=born_location, description=description).save()
        return result
    elif model == 'quote':
        result = Quote(quote=quote, author=Author.objects(fullname=author).first(), tags=tags).save()
        return result


def update(pk, model, fullname='', born_date='', born_location='', description='', quote='', author='', tags=''):
    if model == 'author':
        obj = Author.objects(id=pk).first()
        if obj:
            Author(fullname=fullname, born_date=born_date, born_location=born_location, description=description).reload()
        return obj
    if model == 'quote':
        obj = Quote.objects(id=pk).first()
        if obj:
            Quote(quote=quote, author=Author.objects(fullname=author).first(), tags=tags).reload()
        return obj


def delete(pk, model):
    obj = None
    if model == 'author':
        obj = Author.objects(id=pk).first()
    elif model == 'quote':
        obj = Quote.objects(id=pk).first()

    obj.delete()
    return obj


def main():
    if action == 'create':
        if model == 'author':
            result = create(fullname, born_date, born_location, description)
            print(result.to_mongo().to_dict())
        elif model == 'quote':
            result = create(model, quote, author, tags)
            print(result.to_mongo().to_dict())
    elif action == 'update':
        if model == 'author':
            result = update(pk, fullname, born_date, born_location, description)
            print(result.to_mongo().to_dict()) if result else None
        elif model == 'quote':
            result = update(pk, model, quote, author, tags)
            print(result.to_mongo().to_dict()) if result else None
    elif action == 'read':
        result = find(model)
        print([e.to_mongo().to_dict() for e in result])
    elif action == 'delete':
        result = delete(pk, model)
        print(result.to_mongo().to_dict()) if result else None
    elif action == 'upload':
        result = upload_from_file(filepath, model)
        print(result) if result else None
    else:
        print('Incorrect action')


if __name__ == '__main__':
    main()
