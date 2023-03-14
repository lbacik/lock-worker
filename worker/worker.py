
import requests
import os
import argparse

from string import ascii_letters
from time import sleep
from random import choice, randint


backend_url: str = ''


def worker():
    password = do_request("GET", backend_url + '/get-password')
    print(f'got password: {password}')

    sleep(randint(1, 5))

    response = do_request("POST", backend_url + '/send-request', {'password': password['password']})
    print(f'got response: {response}')

    new_password = ''.join([choice(ascii_letters) for _ in range(4)])
    do_request("PUT", backend_url + '/set-password', {'password': new_password})
    print(f'set new password: {new_password}')


def do_request(method, url, data=None):
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


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--backend-url', type=str, default=None)
    args = argparser.parse_args()
    backend_url = args.backend_url or os.getenv('BACKEND_URL') or ''
    while True:
        worker()

