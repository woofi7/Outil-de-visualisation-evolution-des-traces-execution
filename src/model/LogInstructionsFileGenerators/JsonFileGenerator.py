import json

from model.LogInstructionsFileGenerators.LogInstructionsFileGenerator import LogInstructionsFileGenerator

class JsonFileGenerator(LogInstructionsFileGenerator):

    def __init__(self):
        # Initialisation de la classe
        super().__init__()
    
    def createFile(self, log_instructions, path):
        with open(path, 'w') as f:
            json.dump([log.to_dict() for log in log_instructions], f)