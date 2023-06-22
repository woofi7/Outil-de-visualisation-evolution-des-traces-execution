from pydriller import Repository
import traceback
from view.PopupView import PopupManager

SEARCHED_STRING = "LOG4J"
SEARCHED_FILES = ['.java', '.py']

class LogInstructionDiffGenerator:
    def getCommitChanges(self, commits):
        try:
            result = []  # Initialize an empty list to store the result
            for modification in commits:
                    if [modification.hash, modification.filename, modification.beforeCode, modification.afterCode] not in result:
                         result.append([modification.hash, modification.filename, modification.beforeCode, modification.afterCode])
                         
            print(len(result))
            return result  # Return the list of commits that match the criteria
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_info_popup("Caught Error", str(e))
