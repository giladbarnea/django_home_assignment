#!/usr/bin/env python3.8


def main(msg_id):
    import requests
    url = f"http://localhost:8000/delete"
    if msg_id:
        url += f"/{msg_id}"
    
    headers = {
        'X-CSRFToken':  '2Q2QAtNm2YIoaaVW17Pi2lDF3dYai9cfs4eso1O0RNn1gfuziKCRdR8qZ60yP9R6',
        'Content-Type': 'application/json',
        'Cookie':       'csrftoken=2Q2QAtNm2YIoaaVW17Pi2lDF3dYai9cfs4eso1O0RNn1gfuziKCRdR8qZ60yP9R6',
        
        }
    
    response = requests.request("GET", url, headers=headers)
    
    print(response.text)


def help():
    print(f"""
    delete.py MSG_ID

    Utility to test /delete/... functionality

    MSG_ID
        A number.

    EXAMPLES
        delete.py 42
    """)


def shorthelp():
    print("""delete.py MSG_ID
    Pass "-h" or "--help" for usage instructions.""")


if __name__ == '__main__':
    import sys
    
    msg_id = None
    
    for arg in sys.argv[1:]:
        if arg == '-h' or 'help' in arg:
            help()
            sys.exit(0)
    try:
        msg_id = sys.argv[1]
    except IndexError:
        print('ERROR: must specify MSG_ID')
        help()
    
    main(msg_id)
