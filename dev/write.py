#!/usr/bin/env python3.8


def main(_sender, _receiver, _message, _subject, _localhost: bool, _port):
    import requests
    import json
    if _localhost:
        _url = f"http://localhost:{_port}/write/"
        csrftoken = '2Q2QAtNm2YIoaaVW17Pi2lDF3dYai9cfs4eso1O0RNn1gfuziKCRdR8qZ60yP9R6'
    else:
        _url = f"https://django-home-task-gb.herokuapp.com/write/"
        csrftoken = '9IqrE26wnoaEqHSIradW4AGYCfsc1nk0AapP14xtSPcOlZEP0NHuXrNq9NwcptfE'
    
    headers = {
        'X-CSRFToken':  csrftoken,
        'Content-Type': 'application/json',
        # 'Cookie':       f'csrftoken={csrftoken}',
        
        }
    print('\n', f'{_sender = }', f'{_receiver = }', f'{_message = }', f'{_subject = }', f'{headers = }', sep='\n', end='\n')
    response = requests.request("POST", _url, headers=headers, data=json.dumps({
        "sender":   _sender,
        "receiver": _receiver,
        "message":  _message,
        "subject":  _subject
        }))
    
    print(response.text)


def help():
    print(f"""
    write.py --sender=SENDER --receiver=RECEIVER [OPTIONS]
    
    Utility to test /write/... functionality

    SENDER, RECEIVER
        A username.

    OPTIONS
        --message=MESSAGE       defaults to current date time, e.g. 'Sun Dec 20 22:59:50 2020'
        --subject=SUBJECT       defaults to some random nordish-looking words
        --localhost [--port=PORT]       Sets url to http://localhost:<PORT>/delete. PORT defaults to 8000.
                                        If unspecified, url is https://django-home-task-gb.herokuapp.com/delete

    EXAMPLES
        write.py --sender=john --receiver=daniel
        write.py --sender=john --receiver=daniel --localhost --port=8001
        write.py --sender=john --receiver=daniel --message='Hello World'
        write.py --sender=john --receiver=daniel --subject='Hello' --message='World'
    """)


def shorthelp():
    print("""write.py --sender=SENDER --receiver=RECEIVER [OPTIONS]
    Pass "-h" or "--help" for usage instructions.""")


if __name__ == '__main__':
    import random
    
    
    def randstr():
        """Returns a random string, 15~25 chars long, with some spaces thrown in, that looks like e.g. 'Ivur au wiyqea'"""
        firstletter = string.ascii_uppercase[random.randint(0, len(string.ascii_uppercase) - 1)]
        otherletters = []
        vowels = ['a', 'e', 'i', 'u', 'o']
        for i in range(random.randint(2, 12)):
            letter = string.ascii_lowercase[random.randint(0, len(string.ascii_lowercase) - 1)]
            otherletters.append(letter)
            lastletter = otherletters[-1]
            
            if lastletter != ' ' and random.random() < 0.3:
                otherletters.append(' ')
            
            if lastletter not in vowels and random.random() < 0.3:
                otherletters.append(random.choice(vowels))
        return (firstletter + ''.join(otherletters)).strip()
    
    
    import sys
    import time
    
    import string
    
    sender = None
    receiver = None
    message = time.strftime("%c")
    subject = randstr()
    localhost = False
    port = None
    for arg in sys.argv[1:]:
        if arg == '-h' or 'help' in arg:
            help()
            sys.exit(0)
        if arg.startswith('--sender='):
            sender = arg[9:]
        elif arg.startswith('--receiver='):
            receiver = arg[11:]
        elif arg.startswith('--message='):
            message = arg[10:]
        elif arg.startswith('--subject='):
            subject = arg[10:]
        elif arg.startswith('--localhost'):
            localhost = True
            port = 8000
        elif arg.startswith('--port='):
            port = arg[7:]
        else:
            print(f"WARN: unknown arg '{arg}'")
            help()
            sys.exit(1)
    if not sender or not receiver:
        print('ERROR: must specify "--sender=SENDER" and "--receiver=RECEIVER"')
        help()
    else:
        shorthelp()
    main(sender, receiver, message, subject, localhost, port)
