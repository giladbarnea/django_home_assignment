#!/usr/bin/env python3.8


def main(msg_id, localhost: bool, port):
    import requests
    if localhost:
        url = f"http://localhost:{port}/delete"
    else:
        url = f"https://django-home-task-gb.herokuapp.com/delete"
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
    delete.py MSG_ID [OPTIONS]

    Utility to test /delete/... functionality

    MSG_ID
        A number.

    OPTIONS
        --localhost [--port=PORT]       Sets url to http://localhost:<PORT>/delete. PORT defaults to 8000.
                                        If unspecified, url is https://django-home-task-gb.herokuapp.com/delete
    EXAMPLES
        delete.py 42
        delete.py 42 --localhost --port=8001
    """)


def shorthelp():
    print("""delete.py MSG_ID
    Pass "-h" or "--help" for usage instructions.""")


if __name__ == '__main__':
    import sys
    
    msg_id = None
    localhost = False
    port = None
    for arg in sys.argv[1:]:
        if arg == '-h' or 'help' in arg:
            help()
            sys.exit(0)
        elif arg.startswith('--localhost'):
            localhost = True
            port = 8000
        elif arg.startswith('--port='):
            port = arg[7:]
    try:
        msg_id = sys.argv[1]
    except IndexError:
        print('ERROR: must specify MSG_ID')
        help()
    
    main(msg_id, localhost, port)
