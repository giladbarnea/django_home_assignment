from django.shortcuts import render, HttpResponse


def index(request, *args, **kwargs):
    print(f'index(args: {args}, kwargs: {kwargs})')
    return "Hello from index"
