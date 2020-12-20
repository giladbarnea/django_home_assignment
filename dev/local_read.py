#!/usr/bin/env python3.8


def main(read_endpoint, subpath, queryfilter):
    import requests
    url = f"http://localhost:8000/read"
    if read_endpoint:
        url += f"/{read_endpoint}"
    if subpath:
        url += f"/{subpath}"
    if queryfilter:
        url += f"/{queryfilter}"
    
    headers = {
        'X-CSRFToken':  '2Q2QAtNm2YIoaaVW17Pi2lDF3dYai9cfs4eso1O0RNn1gfuziKCRdR8qZ60yP9R6',
        'Content-Type': 'application/json',
        'Cookie':       'csrftoken=2Q2QAtNm2YIoaaVW17Pi2lDF3dYai9cfs4eso1O0RNn1gfuziKCRdR8qZ60yP9R6',
        
        }
    
    response = requests.request("GET", url, headers=headers)
    
    print(response.text)


def help():
    print(f"""
    local_read.py READ_ENDPOINT SUBPATH [OPTIONS]
    Utility to test /read/... functionality
    
    READ_ENDPOINT
        must be either 'user' or 'msg'
    
    SUBPATH
        if READ_ENDPOINT is 'user', then SUBPATH has to be the username
        if READ_ENDPOINT is 'msg', then SUBPATH has to be the message id
    
    OPTIONS
        --filter=FILTER is available if READ_ENDPOINT is 'user'.
        
    EXAMPLES
        local_read.py user --username=john
        local_read.py user --username=john --filter='read=false'
        local_read.py user --username=john --filter='(read=false AND receiver=daniel)'
    """)


def shorthelp():
    print("""local_read.py READ_ENDPOINT SUBPATH [OPTIONS]
    Pass "-h" or "--help" for usage instructions.""")


if __name__ == '__main__':
    import sys
    
    read_endpoint = None  # 'user' or 'msg'
    subpath = None  # username or message id
    
    queryfilter = None
    for arg in sys.argv[1:]:
        if arg == '-h' or 'help' in arg:
            help()
            sys.exit(0)
        if arg == 'user':
            read_endpoint = 'user'
        if arg.startswith('--username='):
            subpath = arg[11:]
        if arg.startswith('--filter='):
            queryfilter = arg[9:]
        if arg == 'msg':
            read_endpoint = 'msg'
        if arg.startswith('--msg_id='):
            subpath = arg[9:]
    
    if read_endpoint == 'msg' and queryfilter is not None:
        print(f'WARN: {read_endpoint = } and "--filter" was specified; it will have no effect.')
    if read_endpoint is None:
        help()
    else:
        shorthelp()
    
    main(read_endpoint, subpath, queryfilter)
