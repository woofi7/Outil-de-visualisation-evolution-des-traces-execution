from abc import ABC, abstractmethod

class LogInstructionsFileGenerator(ABC):

    @abstractmethod
    def createFile(self, log_instructions):
        pass

