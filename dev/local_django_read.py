#!/usr/bin/env python3.8


def main(read_endpoint, username, queryfilter=None):
    import requests
    url = f"http://localhost:8000/read/{read_endpoint}/{username}"
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
    
    read_endpoint = None  # 'user' or 'msg'
    subpath = None  # username or message id
    
    queryfilter = None
    for arg in sys.argv[1:]:
        if arg == 'user' or arg == '--user':
            read_endpoint = 'user'
        if arg.startswith('--username='):
            subpath = arg[11:]
        if arg.startswith('--filter='):
            queryfilter = arg[9:]
        if arg == 'msg' or arg == '--msg':
            read_endpoint = 'msg'
        if arg.startswith('--msg_id='):
            subpath = arg[9:]
    if not read_endpoint:
        print('FAIL: must specify either "--user" or "--msg" (read endpoint)')
    if not subpath:
        print('FAIL: must specify either "--username=USERNAME" or "--msg_id=MSGID" (subpath)')
    if read_endpoint == 'msg' and queryfilter is not None:
        print(f'WARN: {read_endpoint = } and queryfilter was specified; it will have no effect (queryfilter is only relevant to user)')
    main(read_endpoint, subpath, queryfilter)
