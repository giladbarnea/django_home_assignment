#!/usr/bin/env python3.8
import requests
import json
import time

url = "http://127.0.0.1:8000/write/"

headers = {
    'X-CSRFToken':  '2Q2QAtNm2YIoaaVW17Pi2lDF3dYai9cfs4eso1O0RNn1gfuziKCRdR8qZ60yP9R6',
    'Content-Type': 'application/json',
    'Cookie':       'csrftoken=2Q2QAtNm2YIoaaVW17Pi2lDF3dYai9cfs4eso1O0RNn1gfuziKCRdR8qZ60yP9R6',
    
    }

response = requests.request("POST", url, headers=headers, data=json.dumps({
    "sender":   "catta",
    "receiver": "morki",
    "message":  time.strftime("%T"),
    "subject":  "Greeting"
    }))

print(response.text)
