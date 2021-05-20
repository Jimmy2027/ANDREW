import configparser
import warnings
from contextlib import contextmanager
from pathlib import Path
from time import time

import numpy as np
import requests


def get_readable_elapsed_time(elapsed_time: float, start_msg: str = None) -> str:
    nbr_days = np.round(elapsed_time / (60 * 60 * 24), 5)
    nbr_hours = np.round(elapsed_time / (60 * 60), 5)
    nbr_minutes = np.round(elapsed_time / 60, 5)

    t = start_msg or 'The run took '
    if nbr_days > 3:
        return t + f'{nbr_days} days.'
    elif nbr_hours > 1:
        return t + f'{nbr_hours} hours.'
    elif nbr_minutes > 1:
        return t + f'{nbr_minutes} minutes.'
    else:
        return t + f'{elapsed_time} seconds.'


@contextmanager
def norby(start_message: str = None, end_message: str = None, whichbot: str = None) -> None:
    """
    Context that alerts when context starts, finishes and reports errors.
    """
    start_message = start_message or 'Starting workflow.'

    send_msg(start_message, True, whichbot)
    try:
        start_time = time()
        yield
        elapsed_time = time() - start_time
        time_msg = get_readable_elapsed_time(elapsed_time)
        end_message = end_message or 'Workflow just finished.'
        end_message = ' '.join([end_message, time_msg])
        send_msg(end_message, True, whichbot)
    except Exception as e:
        elapsed_time = time() - start_time
        time_msg = get_readable_elapsed_time(elapsed_time, 'It lived for ')
        error_message = f'Workflow failed. {time_msg}. Sorry for your loss. \n\n {e}'
        send_msg(error_message, True, whichbot)
        raise e


@contextmanager
def maybe_norby(use_norby: bool, start_message: str = None, end_message: str = None, whichbot: str = None) -> None:
    """Norby contextmanager that uses the norby contextmanager if use_norby is True."""
    if not use_norby:
        yield
    else:
        with norby(start_message, end_message, whichbot=whichbot):
            yield


def get_config_path() -> Path:
    """Get the config path."""

    config_path = Path('~/.config/norby_config.ini').expanduser()
    assert config_path.exists(), f'Config file not found under {config_path}. ' \
                                 f'Please fill the example under config and move it to {config_path}.'

    return config_path


def get_config():
    """Read the config and return it as a configparser object."""
    config_path = get_config_path()
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def send_msg(message: str, add_loc_name: bool = False, whichbot: str = None):
    """
    Send message to telegram chat bot.

    message str: text message to be sent to the chat bot.$
    add_loc_name: boolean indicating if the loc_name information should be added to the message. If true the string
        "From {config["other"]["loc_name"]}" will be added at the beginning of the message.
    whichbot str: name of the bot that is to be used to send the message. Defaults to "default".
        See example config under config/norby_config.ini for more info.
    """
    if not whichbot:
        whichbot = 'default'

    config = get_config()
    if f'telegram_bot.{whichbot}' not in config:
        warnings.warn(f'Bot {whichbot} was not found in config. Using default bot.')
        whichbot = 'default'
    token = config[f'telegram_bot.{whichbot}']['token']
    chat_id = config[f'telegram_bot.{whichbot}']['chat_id']
    if add_loc_name:
        message = f'From {config["other"]["loc_name"]}: ' + message
    url_req = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}'
    result = requests.get(url_req)
    if result == '<Response [404]>':
        warnings.warn(f'Could not contact Norby, error: {result} \n url_req: {url_req}')


if __name__ == '__main__':
    with maybe_norby(True, "List Comprehension Example", whichbot='sdfgh'):
        s = [x for x in range(10_000_000)]
