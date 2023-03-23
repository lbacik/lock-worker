
from .redis_mutex import RedisMutex
from ..lock_abc import Lock


class RedisReaderLock(RedisMutex):

    READRES_COUNT = 'readers_count'

    def __init__(self,
                 writer_lock: Lock,
                 name: str = 'lock_reader',
                 host: str = 'localhost',
                 port: int = 6379,
                 db: int = 0) -> None:
        super().__init__(name=name, host=host, port=port, db=db)
        self.writer_lock: Lock = writer_lock

    def acquire(self) -> None:
        self._base_acquire()
        count_byte = self.redis.get(self.READRES_COUNT)
        if count_byte is None:
            count_byte = b'0'
        count: int = int(count_byte.decode('utf-8')) + 1
        print(f'acquire reader: count: {count}')
        if count == 1:
            self.writer_lock.acquire()
        self.redis.set(self.READRES_COUNT, count)
        self.lock.release()

    def release(self) -> None:
        self._base_acquire()
        count_byte = self.redis.get(self.READRES_COUNT)
        count: int = int(count_byte.decode('utf-8')) if count_byte else 1
        if count > 0:
            count = count - 1
        print(f'release reader: count: {count}')
        if count == 0:
            self.writer_lock.release()
        self.redis.set(self.READRES_COUNT, count)
        self.lock.release()

    def _base_acquire(self) -> None:
        while not self.lock.acquire(blocking=True):
            print(f'Waiting for lock {self.name}...')
        print(f'Lock {self.name} acquired')

