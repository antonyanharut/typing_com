import configparser
import os

config = configparser.ConfigParser()
config.read('credentials/google/accounts.ini')
browser = os.environ["BROWSER"]


def email() -> str:
    global config
    return config[browser]['email']


def password() -> str:
    global config
    return config[browser]['password']


def name() -> str:
    global config
    return config[browser]['name']
