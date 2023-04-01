import os
import argparse

from dotenv import load_dotenv
from .lock_factory import LockFactory, NO_LOCK
from .lock.redis_mutex import RedisMutex
from .worker import worker
from .request import set_backend_url


backend_url: str = ''
ttl: int = 0


load_dotenv()


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--backend-url', type=str, default=None)
    argparser.add_argument('--lock', type=str, default=None)
    argparser.add_argument('--ttl', type=int, default=0)
    args = argparser.parse_args()

    backend_url = args.backend_url or os.getenv('BACKEND_URL') or ''
    set_backend_url(backend_url)

    lock_name = args.lock or os.getenv('LOCK') or NO_LOCK
    print(f'lock: {lock_name}')

    ttl: int = int(args.ttl)
    if ttl == 0:
        new_ttl = os.getenv('TTL') or 0
        if int(new_ttl) != 0:
            ttl = int(new_ttl)

    [reader_lock, writer_lock] = LockFactory.create_read_write_lock(lock_name)
    if ttl > 0:
        if not isinstance(writer_lock, RedisMutex):
            raise Exception('ttl is only available for redis locks')
        print(f'create lock with ttl: {ttl}')
        writer_lock = LockFactory.create_lock_with_ttl(writer_lock, ttl)

    while True:
        worker(reader_lock, writer_lock)

