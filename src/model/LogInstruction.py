class LogInstruction:
    def __init__(self, instruction, modifications):
        self.instruction = instruction
        self.modifications = modifications
    
    def add_modification(self, modification):
        self.modifications.append(modification)