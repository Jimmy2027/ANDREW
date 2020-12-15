# HK, 15.12.20

import warnings
import requests


def send_msg(message: str, config):
    token = config['telegram_bot']['token']
    chat_id = config['telegram_bot']['chat_id']
    url_req = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}'
    result = requests.get(url_req)
    if result == '<Response [404]>':
        warnings.warn(f'Could not contact Norby, error: {result} \n url_req: {url_req}')
