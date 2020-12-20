#!/usr/bin/env python3.8


def main(sender, receiver, message, subject):
    import requests
    import json
    url = "http://127.0.0.1:8000/write/"
    
    headers = {
        'X-CSRFToken':  '2Q2QAtNm2YIoaaVW17Pi2lDF3dYai9cfs4eso1O0RNn1gfuziKCRdR8qZ60yP9R6',
        'Content-Type': 'application/json',
        'Cookie':       'csrftoken=2Q2QAtNm2YIoaaVW17Pi2lDF3dYai9cfs4eso1O0RNn1gfuziKCRdR8qZ60yP9R6',
        
        }
    print('\n', f'{sender = }', f'{receiver = }', f'{message = }', f'{subject = }', sep='\n', end='\n')
    response = requests.request("POST", url, headers=headers, data=json.dumps({
        "sender":   sender,
        "receiver": receiver,
        "message":  message,
        "subject":  subject
        }))
    
    print(response.text)


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
    message = time.strftime("%T")
    subject = randstr()
    for arg in sys.argv[1:]:
        if arg.startswith('--sender='):
            sender = arg[9:]
        if arg.startswith('--receiver='):
            receiver = arg[11:]
        if arg.startswith('--message='):
            message = arg[10:]
        if arg.startswith('--subject='):
            subject = arg[10:]
    if not sender:
        print('FAIL: must specify "--sender=SENDER"')
    if not receiver:
        print('FAIL: must specify "--receiver=RECEIVER"')
    main(sender, receiver, message, subject)
