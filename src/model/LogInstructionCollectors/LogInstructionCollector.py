from abc import ABC, abstractmethod

class LogInstructionCollector(ABC):

    @abstractmethod
    def get_log_instructions(self, repo_path, path_in_directory, branch, author):
        pass

