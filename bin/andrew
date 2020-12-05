#!/usr/bin/env python3

import argparse
import subprocess
import time
import configparser
import requests
from pathlib import Path
import os

# Reading the config
config_path = Path(os.path.expanduser('~/.config/andrew_config.ini'))
assert config_path.exists(), f'Config file not found under {config_path}. ' \
                             f'Please fill the example under config and move it to {config_path}.'

config = configparser.ConfigParser()
config.read(config_path)

# parsing the arguments
parser = argparse.ArgumentParser()
parser.add_argument('command', type=str, help='command to be exectued')
input = parser.parse_args()


def send_msg(message):
    token = config['telegram_bot']['token']
    chat_id = config['telegram_bot']['chat_id']
    url_req = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}'
    requests.get(url_req)


start_time = time.time()
print(f'executing command {input.command}')
try:
    output = subprocess.check_output(input.command, shell=True)
    duration = time.time() - start_time
    message = f'Job {input.command} at {config["other"]["loc_name"]} just finished. It took {duration} seconds or {duration // 60} minutes. \n ' \
              f'The output is: \n\n {output.rstrip()}'
except Exception as e:
    duration = time.time() - start_time
    message = f'your job got killed with: \n {e} \n It lived for {duration} seconds. Sorry for your loss.'
send_msg(message)
