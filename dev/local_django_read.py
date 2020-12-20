#!/usr/bin/env python3.8


def main(username, queryfilter=None):
    import requests
    url = f"http://localhost:8000/read/user/{username}"
    if queryfilter:
        url += f"/{queryfilter}"
    
    headers = {
        'X-CSRFToken':  '2Q2QAtNm2YIoaaVW17Pi2lDF3dYai9cfs4eso1O0RNn1gfuziKCRdR8qZ60yP9R6',
        'Content-Type': 'application/json',
        'Cookie':       'csrftoken=2Q2QAtNm2YIoaaVW17Pi2lDF3dYai9cfs4eso1O0RNn1gfuziKCRdR8qZ60yP9R6',
        
        }
    
    response = requests.request("GET", url, headers=headers)
    
    print(response.text)


if __name__ == '__main__':
    import sys
    
    username = 'morki'
    queryfilter = None
    for arg in sys.argv[1:]:
        if arg.startswith('--username='):
            username = arg[11:]
        if arg.startswith('--filter='):
            queryfilter = arg[9:]
    main(username, queryfilter)
