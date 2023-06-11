import traceback
from view.PopupView import PopupManager

class Modification:
    def __init__(self, commit, date, type) :
        try:
            self.commit = commit
            self.date = date
            self.type = type
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))
    
    def get_commit_hash(self):
        try:
            return self.commit
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))
    
    def get_date(self):
        try:
            return self.date
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))