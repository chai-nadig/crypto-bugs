import os

import requests

lines = []


def batch_telegram_messages():
    def decorator_func(func):
        def wrapper_func(*args, **kwargs):
            retval = func(*args, **kwargs)
            _send('\n'.join(get_lines()))
            clear_lines()
            return retval

        return wrapper_func

    return decorator_func


def get_lines():
    return lines


def clear_lines():
    global lines
    lines = []


def send_message(content):
    print(content)
    lines.append(content)


def _send(content):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)

    payload = {
        'parse_mode': 'HTML',
        'chat_id': chat_id,
        'text': content,
    }
    r = requests.get(url, params=payload)

    if r.status_code != 200:
        print("error sending telegram msg", r.content.decode('utf-8'))
