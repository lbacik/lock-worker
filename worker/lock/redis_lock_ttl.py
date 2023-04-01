from redis import Redis
import time
from ..lock_abc import Lock

class RedisLockWithTtl(Lock):

    def __init__(self,
        lock: Lock,
        ttl: int,
        host: str = 'localhost',
        port: int = 6379,
        db: int = 0,
        name: str = 'writer_ttl',
    ) -> None:
        self.redis: Redis[bytes] = Redis(host=host, port=port, db=db)
        self.lock: Lock = lock
        self.ttl: int = ttl
        self.name: str = name
        self.last_change_timer_value: int = 0

    def acquire(self) -> None:
        if self._is_time_for_change():
            self.lock.acquire()
            if self._is_time_for_change() is False:
                self.lock.release()
                raise Exception('Password already changed')
            self._reset_timer()
        else:
            raise Exception('Not time for change password')

    def release(self) -> None:
        self.lock.release()

    def _is_time_for_change(self) -> bool:
        timer_value = self._get_timer_value()
        if timer_value:
            if timer_value > self.ttl:
                self.last_change_timer_value = timer_value
                return True
        else:
            self._reset_timer()
        return False

    def _get_timer_value(self) -> int | None:
        result: int | None = None
        value: bytes | None = self.redis.get(self.name)
        if value:
            start_time = int(value.decode('utf-8'))
            current_time: int = int(time.time())
            result = current_time - start_time
        return result

    def _reset_timer(self) -> None:
        self.redis.set(self.name, int(time.time()))

