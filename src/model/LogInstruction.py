class LogInstruction:
    def __init__(self, instruction, modifications):
        self.instruction = instruction
        if modifications is None:
            self.modifications = []
        else:
            self.modifications = modifications
    
    def add_modification(self, modification):
        if(self.modifications is not None):
            self.modifications.append(modification)