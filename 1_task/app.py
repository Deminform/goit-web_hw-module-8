import argparse
import json
import re
import sys

import redis
from bson import ObjectId
from redis_lru import RedisLRU
from decorators import error_decorator

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

parser = argparse.ArgumentParser(description='Python Web / Homework / Module 8')
parser.add_argument('-a', '--action', help='create, update, read, delete, upload', metavar='')
parser.add_argument('-m', '--model', help='author, quote', metavar='')
parser.add_argument('--id', metavar='')
parser.add_argument('--fullname', metavar='')
parser.add_argument('--filepath', metavar='')
parser.add_argument('--born_date', metavar='')
parser.add_argument('--born_location', metavar='')
parser.add_argument('--description', metavar='')
parser.add_argument('--quote', metavar='')
parser.add_argument('--author', metavar='')
parser.add_argument('--tags', nargs='+', metavar='')

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


@error_decorator
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
            result.append((Quote(quote=obj['quote'],
                                 author=Author.objects(fullname=obj['author'])
                                 .first(),
                                 tags=obj['tags']).save()).to_mongo().to_dict())
    return result


@error_decorator
@cache
def find_all(model):
    if model == 'author':
        result = Author.objects.all()
        return result if result else []
    elif model == 'quote':
        result = Quote.objects.all()
        return result if result else []


@error_decorator
@cache
def find_by_name(argument):
    author_r = Author.objects(fullname__istartswith=argument.lower()).first()
    if author_r:
        result = Quote.objects(author=ObjectId(author_r.id)).all()
        return [r.quote for r in result]


@error_decorator
@cache
def find_by_tag(argument):
    regex = re.compile(f'^{argument.lower()}.*')
    result = Quote.objects(tags__iregex=regex).all()
    return [r.quote for r in result]


@error_decorator
@cache
def find_by_tags(argument):
    result = Quote.objects(tags__in=argument).all()
    return [r.quote for r in result]


@error_decorator
def create(model, fullname='', born_date='', born_location='', description='', quote='', author='', tags=''):
    if model == 'author':
        result = Author(fullname=fullname,
                        born_date=born_date,
                        born_location=born_location,
                        description=description).save()
        return result
    elif model == 'quote':
        author_r = Author.objects(fullname=author).first()
        if author_r:
            result = Quote(quote=quote,
                           author=author_r.id,
                           tags=tags).save()
            return result


@error_decorator
def update(pk, model, fullname='', born_date='', born_location='', description='', quote='', author='', tags=''):
    if model == 'author':
        obj = Author.objects(id=pk).first()
        if obj:
            result = obj.update(set__fullname=fullname,
                                set__born_date=born_date,
                                set__born_location=born_location,
                                set__description=description)
            return result if result else None
    if model == 'quote':
        obj = Quote.objects(id=pk).first()
        if obj:
            result = obj.update(quote=quote,
                                author=Author.objects(fullname=author).first(),
                                tags=tags)
            return result if result else None


@error_decorator
def delete(pk, model):
    obj = None
    if model == 'author':
        obj = Author.objects(id=pk).first()
    elif model == 'quote':
        obj = Quote.objects(id=pk).first()

    obj.delete()
    return obj


def main():
    if action in ('create', 'read', 'delete', 'update', 'upload') and model in ('author', 'quote'):
        if action == 'create':
            if model == 'author':
                result = create(model=model,
                                fullname=fullname,
                                born_date=born_date,
                                born_location=born_location,
                                description=description)
                print(result)
            elif model == 'quote':
                result = create(model=model,
                                quote=quote,
                                author=author,
                                tags=tags)
                print(result.to_mongo().to_dict())
        elif action == 'update':
            if model == 'author':
                result = update(pk=pk,
                                model=model,
                                fullname=fullname,
                                born_date=born_date,
                                born_location=born_location,
                                description=description)
                print(result)
            elif model == 'quote':
                result = update(pk=pk,
                                model=model,
                                quote=quote,
                                author=author,
                                tags=tags)
                print(result)
        elif action == 'read':
            result = find_all(model)
            print([e.to_mongo().to_dict() for e in result])
        elif action == 'delete':
            result = delete(pk, model)
            print(result)
        elif action == 'upload':
            result = upload_from_file(filepath, model)
            print(result)
        else:
            print('Incorrect action')
    else:
        print('Incorrect command\navailable actions: create, read, delete, --upload\navailable models: author, quote')


def detach():
    while True:
        command = input('Enter a command or type "exit" or keep empty to exit: ')
        command, argument = command.split(':', 1) if len(command.split(':')) > 1 else exit(0)
        match command:
            case 'name':
                result = find_by_name(argument.strip()) if argument else print('Please enter author name for search.')
                print(result) if result else print('No results found for your request.')
            case 'tag':
                result = find_by_tag(argument.strip()) if argument else print('Enter text for search.')
                print(result) if result else print('No results found for your request.')
            case 'tags':
                result = find_by_tags((argument.split(','))) if argument else print('Enter text for search.')
                print(result) if result else print('No results found for your request.')
            case 'exit':
                break


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        detach()
    else:
        main()
