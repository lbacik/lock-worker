
from ..lock_abc import Lock


class FakeLock(Lock):

    def acquire(self) -> None:
        pass

    def release(self) -> None:
        pass
