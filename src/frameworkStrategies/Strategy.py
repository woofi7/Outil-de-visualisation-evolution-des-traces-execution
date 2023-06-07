from abc import ABC, abstractmethod

class AbstractClass(ABC):
    
    # Function to get the logs specific to a framework
    @abstractmethod
    def getLogs(self):
        pass
