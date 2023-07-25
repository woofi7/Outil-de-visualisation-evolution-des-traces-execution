import traceback
from model.LogInstructionCollectors.Modification import Modification

class LogInstruction:
    def __init__(self,level ,instruction, modifications, date):
        self.level = level
        self.instruction = instruction
        self.date = date
        if modifications is None:
            self.modifications = []
        else:
            self.modifications = modifications
    
    def add_modification(self, modification):
        if(self.modifications is not None):
            self.modifications.append(modification)
            
    def copy(self):
        logInstructionCopy = LogInstruction(self.level, self.instruction, [], self.date)
        for modification in self.modifications:
            logInstructionCopy.add_modification(Modification(modification.level, modification.instruction, modification.date, modification.type, modification.beforeCode, modification.afterCode, modification.hash, modification.filename, modification.author))
        return logInstructionCopy