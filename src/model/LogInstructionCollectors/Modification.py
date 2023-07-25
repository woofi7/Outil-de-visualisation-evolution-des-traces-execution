import traceback
from view.PopupView import PopupManager

class Modification:
    def __init__(self, level, instruction, date, type, beforeCode, afterCode, hash, filename, author) :
        self.level = level
        self.instruction = instruction
        self.date = date
        self.type = type
        self.beforeCode = beforeCode
        self.afterCode = afterCode
        self.hash = hash
        self.filename = filename
        self.author = author
    
    def get_commit_hash(self):
        return self.hash
    
    def get_date(self):
        return self.date