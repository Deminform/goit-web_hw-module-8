import argparse
import json
import re

from bson import ObjectId

from conf import connect

from conf.models import Author, Quote

parser = argparse.ArgumentParser(description='Python Web / Homework / Module 8')
parser.add_argument('--action', help='create, update, read, delete, upload', metavar='')
parser.add_argument('--model', help='author, quote', metavar='')
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


def find_all(model):
    if model == 'author':
        return Author.objects.all()
    elif model == 'quote':
        return Quote.objects.all()


def find_by_name(argument):
    result = Author.objects(fullname__istartswith=argument).first()
    return Quote.objects(author=ObjectId(result.id)).all()
#
#
# def find_by_name(argument):
#     result = Author.objects(fullname=argument).first()
#     return Quote.objects(author=ObjectId(result.id)).all()

#
# def find_by_symbols(argument):
#     return Quote.objects(tags__contains=argument).all()


def find_by_tag(argument):
    regex = re.compile(f'^{argument}.*')
    return Quote.objects(tags=regex).all()


def find_by_tags(argument):
    return Quote.objects(tags__in=argument).all()


def create(model, fullname='', born_date='', born_location='', description='', quote='', author='', tags=''):
    if model == 'author':
        return Author(fullname=fullname,
                      born_date=born_date,
                      born_location=born_location,
                      description=description).save()
    elif model == 'quote':
        return Quote(quote=quote,
                     author=Author.objects(fullname=author).first(),
                     tags=tags).save()


def update(pk, model, fullname='', born_date='', born_location='', description='', quote='', author='', tags=''):
    if model == 'author':
        obj = Author.objects(id=pk).first()
        if obj:
            return Author(fullname=fullname,
                          born_date=born_date,
                          born_location=born_location,
                          description=description).reload()
    if model == 'quote':
        obj = Quote.objects(id=pk).first()
        if obj:
            return Quote(quote=quote,
                         author=Author.objects(fullname=author).first(),
                         tags=tags).reload()
    return None


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
        result = find_all(model)
        print([e.to_mongo().to_dict() for e in result])
    elif action == 'delete':
        result = delete(pk, model)
        print(result.to_mongo().to_dict()) if result else None
    elif action == 'upload':
        result = upload_from_file(filepath, model)
        print(result) if result else None
    else:
        while True:
            command = input('Enter a command or type "exit" or keep empty to exit: ')
            command, argument = command.split(':', 1) if command else exit(0)
            match command:
                case 'name':
                    quotes = find_by_name(argument.strip())
                    print([el.to_mongo().to_dict() for el in quotes])
                case 'tag':
                    quotes = find_by_tag(argument.strip())
                    print([el.to_mongo().to_dict() for el in quotes])
                case 'tags':
                    quotes = find_by_tags((argument.split(',')))
                    print([el.to_mongo().to_dict() for el in quotes])
                case 'exit':
                    break


if __name__ == '__main__':
    main()
