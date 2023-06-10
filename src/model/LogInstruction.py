import traceback
from view.PopupView import PopupManager

class LogInstruction:
    def __init__(self, instruction, modifications, date):
        try:
            self.instruction = instruction
            self.date = date
            if modifications is None:
                self.modifications = []
            else:
                self.modifications = modifications
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))
    
    def add_modification(self, modification):
        try:
            if(self.modifications is not None):
                self.modifications.append(modification)
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))