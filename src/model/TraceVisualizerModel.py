from pydriller import Repository
import traceback
from view.PopupView import PopupManager

SEARCHED_STRING = "LOG4J"
SEARCHED_FILES = ['.java', '.py']

class TraceVisualizerModel:
    # def getCommitChanges(self, commit_hash, repo_url):
    #     result = []  # Initialize an empty list to store the result
    #     for commit in Repository(repo_url).traverse_commits():
    #         # Check if the commit hash matches the provided commit_hash
    #         if commit.hash.startswith(commit_hash):
    #             for modification in commit.modified_files:
    #                 # Retrieve information about the modified files in the commit
    #                 result.append([commit.hash[:7], modification.filename, modification.source_code_before, modification.source_code])
    #     return result  # Return the list of commits that match the criteria
    def getCommitChanges(self, commits):
        try:
            result = []  # Initialize an empty list to store the result
            # Check if the commit hash matches the provided commit_hash
            # for commit in commits:
            #     #print(commit)
            #     for modification in commit.modified_files:
            #         if [commit.hash[:7], modification.filename, modification.source_code_before, modification.source_code] not in result:
            #             # Retrieve information about the modified files in the commit
            #             result.append([commit.hash[:7], modification.filename, modification.source_code_before, modification.source_code])
            for modification in commits:
                    if [modification.hash, modification.filename, modification.beforeCode, modification.afterCode] not in result:
                         result.append([modification.hash, modification.filename, modification.beforeCode, modification.afterCode])
                         
            print(len(result))
            return result  # Return the list of commits that match the criteria
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))
