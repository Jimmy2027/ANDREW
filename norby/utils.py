# HK, 15.12.20

import warnings
from pathlib import Path
import configparser

import requests

# Reading the config
CONFIG_PATH = Path('~/.config/norby_config.ini').expanduser()
assert CONFIG_PATH.exists(), f'Config file not found under {CONFIG_PATH}. ' \
                             f'Please fill the example under config and move it to {CONFIG_PATH}.'


def get_config():
    config_path = CONFIG_PATH
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def send_msg(message: str, config=None):
    if not config:
        config = get_config()
    token = config['telegram_bot']['token']
    chat_id = config['telegram_bot']['chat_id']
    url_req = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}'
    result = requests.get(url_req)
    if result == '<Response [404]>':
        warnings.warn(f'Could not contact Norby, error: {result} \n url_req: {url_req}')
