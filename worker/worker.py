from string import ascii_letters
from time import sleep
from random import choice, randint
from .lock_abc import Lock
from .lock_factory import *
from .main import do_request


def change_report(lock: Lock, new_password: str) -> None:
    if isinstance(lock, RedisLockWithTtl):
        print(f'set new password: {new_password} after {lock.last_change_timer_value} seconds')
    else:
        print(f'set new password: {new_password}')


def worker(reader: Lock, writer: Lock) -> None:

    reader.acquire()
    password: dict = do_request("GET", '/get-password')
    sleep(randint(1, 3))
    response: dict = do_request("POST", '/send-request', {'password': password.get('password')})
    reader.release()

    print(f'got password: {password}')
    print(f'got response: {response}')

    new_password: str = ''.join([choice(ascii_letters) for _ in range(4)])

    writer.acquire()
    do_request("PUT", '/set-password', {'password': new_password})
    change_report(writer, new_password)
    writer.release()

