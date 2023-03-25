
from .redis_mutex import RedisMutex


class RedisWriterLock(RedisMutex):
    def __init__(self,
                 name: str = 'lock_writer',
                 host: str = 'localhost',
                 port: int = 6379,
                 db: int = 0) -> None:
        super().__init__(name=name, host=host, port=port, db=db)

    def release(self) -> None:
        if self.lock.owned():
           super().release()
        else:
            self.redis.delete(self.name)

