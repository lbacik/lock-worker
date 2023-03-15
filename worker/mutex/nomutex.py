
from ..mutex_abc import Mutex


class NoMutex(Mutex):

    def acquire(self) -> None:
        pass

    def release(self) -> None:
        pass
