import numpy as np
from abc import ABC, abstractmethod

from tournament.connect4.connect_state import ConnectState


class Policy(ABC):
    def __init__(self):
        self
    


    @abstractmethod
    def mount(self) -> None:
        pass

    @abstractmethod
    def act(self, s: np.ndarray) -> int:
        pass
