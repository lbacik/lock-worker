
from .lock_abc import Lock
from .lock.redis_mutex import RedisMutex
from .lock.fake_lock import FakeLock
from .lock.redis_reader_lock import RedisReaderLock
from .lock.redis_writer_lock import RedisWriterLock
from os import getenv
from typing import List


NO_LOCK = 'no-lock'
LOCK_MUTEX = 'mutex'
LOCK_RW = 'rw'


class LockFactory:

        @classmethod
        def create_redis_mutex(cls,
                               name: str,
                               host: str,
                               port: str,
                               db: str) -> Lock:
            return RedisMutex(
                name=name,
                host=host,
                port=int(port),
                db=int(db),
            )

        @classmethod
        def fake_lock(cls) -> Lock:
            return FakeLock()

        @classmethod
        def create_reader_lock(cls, name: str, writer_lock: Lock, host: str, port: str, db: str) -> Lock:
            return RedisReaderLock(name=name, writer_lock=writer_lock, host=host, port=int(port), db=int(db))

        @classmethod
        def create_read_write_lock(cls, lock_name: str) -> List[Lock]:
            if lock_name == LOCK_MUTEX:
                reader_lock: Lock = cls.create_redis_mutex(
                    name='mutex',
                    host=getenv('REDIS_HOST') or 'localhost',
                    port=getenv('REDIS_PORT') or '6379',
                    db=getenv('REDIS_DB') or '0',
                )
                writer_lock: Lock = reader_lock
            elif lock_name == LOCK_RW:
                writer_lock: Lock = RedisWriterLock(
                    host=getenv('REDIS_HOST') or 'localhost',
                    port=getenv('REDIS_PORT') or '6379',
                    db=getenv('REDIS_DB') or '0',
                )
                reader_lock: Lock = cls.create_reader_lock(
                    name='lock_reader',
                    writer_lock=writer_lock,
                    host=getenv('REDIS_HOST') or 'localhost',
                    port=getenv('REDIS_PORT') or '6379',
                    db=getenv('REDIS_DB') or '0',
                )
            else:
                reader_lock: Lock = cls.fake_lock()
                writer_lock: Lock = reader_lock

            return [reader_lock, writer_lock]

