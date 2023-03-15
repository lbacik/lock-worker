
from .mutex_abc import Mutex
from .mutex.redis import RedisMutex
from .mutex.nomutex import NoMutex


class MutexFactory:

        @staticmethod
        def create_redis_mutex(host: str, port: str, db: str) -> Mutex:
            return RedisMutex(host=host, port=int(port), db=int(db))

        @staticmethod
        def no_mutex() -> Mutex:
            return NoMutex()

