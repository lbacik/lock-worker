
from redis import Redis
from redis.lock import Lock
from ..lock_abc import Lock as LockABC


class RedisMutex(LockABC):

    def __init__(self,
                 name: str = 'mutex',
                 host: str = 'localhost',
                 port: int = 6379,
                 db: int = 0) -> None:
        self.redis: Redis[bytes] = Redis(host=host, port=port, db=db)
        self.lock = Lock(self.redis, name, timeout=None, blocking_timeout=5)
        self.name: str = name

    def acquire(self) -> None:
        while not self.lock.acquire(blocking=True):
            print(f'Waiting for lock {self.name}...')
        print(f'Lock {self.name} acquired')

    def release(self) -> None:
        self.lock.release()

