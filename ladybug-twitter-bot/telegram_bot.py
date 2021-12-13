import os

import requests


def send_message(content):
    print(content)
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
