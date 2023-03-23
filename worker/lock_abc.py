from abc import ABC, abstractmethod


class Lock(ABC):

    @abstractmethod
    def acquire(self) -> None:
        pass

    @abstractmethod
    def release(self) -> None:
        pass

