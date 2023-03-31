import os
import requests
import argparse

from dotenv import load_dotenv
from .lock_factory import LockFactory, NO_LOCK
from .worker import worker


backend_url: str = ''
ttl: int = 0


load_dotenv()


def do_request(method: str, uri: str, data=None) -> dict:
    url = backend_url + uri
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
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--backend-url', type=str, default=None)
    argparser.add_argument('--lock', type=str, default=None)
    argparser.add_argument('--ttl', type=int, default=0)
    args = argparser.parse_args()

    backend_url = args.backend_url or os.getenv('BACKEND_URL') or ''
    lock_name = args.lock or os.getenv('LOCK') or NO_LOCK
    ttl: int = int(args.ttl)
    if ttl == 0:
        new_ttl = os.getenv('TTL') or 0
        if int(new_ttl) != 0:
            ttl = int(new_ttl)

    [reader_lock, writer_lock] = LockFactory.create_read_write_lock(lock_name)
    if ttl > 0:
        writer_lock = LockFactory.create_lock_with_ttl(writer_lock, ttl)

    while True:
        worker(reader_lock, writer_lock)

