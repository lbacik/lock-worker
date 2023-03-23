
import requests
import os
import argparse

from string import ascii_letters
from time import sleep
from random import choice, randint
from dotenv import load_dotenv
from .lock_abc import Lock
from .lock_factory import *


backend_url: str = ''
mutex_flag: bool = False


def worker(reader: Lock, writer: Lock) -> None:

    reader.acquire()
    password: dict = do_request("GET", backend_url + '/get-password')
    sleep(randint(1, 3))
    response: dict = do_request("POST", backend_url + '/send-request', {'password': password.get('password')})
    reader.release()

    print(f'got password: {password}')
    print(f'got response: {response}')

    new_password: str = ''.join([choice(ascii_letters) for _ in range(4)])

    writer.acquire()
    do_request("PUT", backend_url + '/set-password', {'password': new_password})
    writer.release()

    print(f'set new password: {new_password}')


def do_request(method, url, data=None) -> dict:
    if method == "GET":
        response = requests.get(url)
    elif method == "POST":
        response = requests.post(url, json=data)
    elif method == "PUT":
        response = requests.put(url, json=data)
    else:
        raise ValueError("Unknown method")

    if response.status_code == 200:
        return response.json()
    else:
        return dict()


if __name__ == '__main__':

    load_dotenv()

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--backend-url', type=str, default=None)
    argparser.add_argument('--lock', type=str, default=None)
    args = argparser.parse_args()

    backend_url = args.backend_url or os.getenv('BACKEND_URL') or ''
    lock_name = args.lock or os.getenv('LOCK') or NO_LOCK

    [reader_lock, writer_lock] = LockFactory.create_read_write_lock(lock_name)

    while True:
        worker(reader_lock, writer_lock)

