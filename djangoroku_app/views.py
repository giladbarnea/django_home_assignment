from django.shortcuts import render, HttpResponse


def index(request, *args, **kwargs):
    print(f'index(args: {args}, kwargs: {kwargs})')
    return HttpResponse(b"Hello from index")


def send_msg(request, *args, **kwargs):
    print(f'send_msg(args: {args}, kwargs: {kwargs})')
    return HttpResponse(b"Hello from send_msg")
