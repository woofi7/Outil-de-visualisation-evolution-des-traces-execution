from abc import ABC, abstractmethod

class AbstractClass(ABC):
    @abstractmethod
    def getLogs(self):
        pass
