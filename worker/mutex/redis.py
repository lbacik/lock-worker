
from redis import Redis
from redis.lock import Lock
from ..mutex_abc import Mutex


class RedisMutex(Mutex):

    MUTEX_KEY_NAME = 'mutex'

    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0) -> None:
        self.redis: Redis[bytes] = Redis(host=host, port=port, db=db)
        self.lock = Lock(self.redis, self.MUTEX_KEY_NAME, timeout=None, blocking_timeout=5)

    def acquire(self) -> None:
        while not self.lock.acquire(blocking=True):
            print('Waiting for lock...')
        print('Lock acquired')

    def release(self) -> None:
        self.lock.release()

