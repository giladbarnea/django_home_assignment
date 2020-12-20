#!/usr/bin/env python3.8


def main(mode, subpath, queryfilter):
    import requests
    url = f"http://localhost:8000/read"
    if mode:
        url += f"/{mode}"
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
    read.py <MODE> <SUBPATH> [OPTIONS]
    
    Utility to test /read/... functionality
    
    MODE
        must be either 'user' or 'msg'
    
    SUBPATH
        if MODE is 'user', then SUBPATH has to be the username
        if MODE is 'msg', then SUBPATH has to be the message id
    
    OPTIONS
        --filter=FILTER is available if MODE is 'user'.
        --msg_id=MSG_ID is available if MODE is 'msg'.
        
    EXAMPLES
        read.py user --username=john
        read.py user --username=john --filter='read=false'
        read.py user --username=john --filter='(read=true AND receiver=daniel)'
        read.py msg --msg_id=42
    """)


def shorthelp():
    print("""read.py MODE SUBPATH [OPTIONS]
    Pass "-h" or "--help" for usage instructions.""")


if __name__ == '__main__':
    import sys
    
    mode = None  # 'user' or 'msg'
    subpath = None  # username or message id
    
    queryfilter = None
    for arg in sys.argv[1:]:
        if arg == '-h' or 'help' in arg:
            help()
            sys.exit(0)
        if arg == 'user':
            mode = 'user'
        elif arg.startswith('--username='):
            subpath = arg[11:]
        elif arg.startswith('--filter='):
            queryfilter = arg[9:]
        elif arg == 'msg':
            mode = 'msg'
        elif arg.startswith('--msg_id=') or arg.startswith('--msg-id='):
            subpath = arg[9:]
        else:
            print(f"WARN: unknown arg '{arg}'")
            help()
    
    if mode == 'msg' and queryfilter is not None:
        print(f'WARN: {mode = } and "--filter" was specified; it will have no effect.')
        help()
    if mode is None:
        print('ERROR: must specify <MODE>')
        help()
    else:
        shorthelp()
    
    main(mode, subpath, queryfilter)
