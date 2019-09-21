import time
from abc import ABC, abstractmethod
from typing import Tuple, Optional, NewType


class Strategy(ABC):
    @abstractmethod
    def parse(self, timespec: str) -> Optional[Tuple[float, time.struct_time]]:
        pass


class TimestampStrategy(Strategy):
    def parse(self, timespec):
        try:
            return [1., time.gmtime(int(timespec))]
        except ValueError:
            return None
