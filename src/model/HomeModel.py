import traceback
from pydriller import Repository
from PyQt6.QtCore import QDate, Qt
from datetime import datetime
from git import Repo
from model.Modification import Modification
from model.LogInstruction import LogInstruction

import shutil
import os
import stat

from view.PopupView import PopupManager

SEARCHED_STRINGS = [".always",".catching", ".critical", ".debug", ".error", ".fatal", ".info", ".warn", ".trace", ".log", ".trace"]
SEARCHED_FILES = ['.java', '.py']
INVALID_STRINGS = ["import", "from", "include", "return", "except"]

class HomeModel:

    def get_log_instructions(self, repo_url, from_date, to_date, searched_path, searched_branch, searched_author):
        try:
            added_log_instructions = []  # Initialize an empty list to store the added log instructions
            deleted_log_instructions = []  # Initialize an empty list to store the deleted log instructions

            # Convert the input dates to datetime objects
            from_date_obj = datetime.strptime(from_date, '%Y-%m-%d')
            to_date_obj = datetime.strptime(to_date, '%Y-%m-%d')

            # Create datetime objects for the start and end dates
            dt1 = datetime(from_date_obj.year, from_date_obj.month, from_date_obj.day)
            dt2 = datetime(to_date_obj.year, to_date_obj.month, to_date_obj.day)

            # Iterate through the commits in the repository
            # for commit in Repository(repo_url, single="9f1bff41fc2ca84e9a2878f03177601d9889f8f9").traverse_commits():
            for commit in Repository(repo_url,since=dt1, to=dt2, only_modifications_with_file_types=SEARCHED_FILES, only_in_branch=searched_branch).traverse_commits():
                if (searched_author == "" or commit.author is searched_author) :
                    # Traverse through the modified files in each commit
                    for modification in commit.modified_files:
                        # Check if the file has an allowed extension
                        if any(modification.filename.endswith(ext) for ext in SEARCHED_FILES) and ((modification.old_path is not None and searched_path in modification.old_path) or (modification.new_path is not None and searched_path in modification.new_path)):
                            # Check if added log instructions are present in the modification
                            is_added_code_log_based, added_code = self.__locate_log_instructions(modification.diff_parsed["added"], SEARCHED_STRINGS, INVALID_STRINGS)
                            # Check if removed log instructions are present in the modification
                            is_removed_code_log_based, removed_code = self.__locate_log_instructions(modification.diff_parsed["deleted"], SEARCHED_STRINGS, INVALID_STRINGS)

                            if is_added_code_log_based:
                                # Create a modification object to add to the log instruction
                                mod_object = Modification(commit, commit.committer_date, "added")

                                # Check if the code already exists in the returning list
                                instruction_index = next((i for i, log_instruction in enumerate(added_log_instructions) if log_instruction.instruction.replace("  ", "") == added_code), None)

                                if instruction_index is not None:
                                    # Add the modification to the existing log instruction
                                    added_log_instructions[instruction_index].add_modification(mod_object)
                                else:
                                    # Create a new log instruction and add it to the list
                                    added_log_instructions.append(LogInstruction(added_code, [mod_object]))
                            if is_removed_code_log_based:
                                # Create a modification object for deleted log instruction
                                mod_object = Modification(commit, commit.committer_date, "deleted")

                                # Check if the instruction already exists in the deleted log instructions
                                instruction_index = next((i for i, log_instruction in enumerate(deleted_log_instructions) if log_instruction.instruction.replace("  ", "") == removed_code), None)
                                if instruction_index is not None:
                                    # Add the modification to the existing log instruction
                                    deleted_log_instructions[instruction_index].add_modification(mod_object)
                                else:
                                    # Create a new log instruction and add it to the list
                                    deleted_log_instructions.append(LogInstruction(removed_code, [mod_object]))
            # Save the lists as properties
            self.added_log_instructions = added_log_instructions
            self.deleted_log_instructions = deleted_log_instructions
            
            # Return the list of log instructions that match the criteria
            return added_log_instructions, deleted_log_instructions
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))

    def __locate_log_instructions(self, modifications_list, target_strings, invalid_strings):
        try:
            my_tuple = None
            for t in modifications_list:
                if isinstance(t, tuple) and any(element in t[1] for element in target_strings) and all(element not in t[1] for element in invalid_strings):
                    my_tuple = t
                    break
            if my_tuple:
                return True, my_tuple[1]
            else:
                return False, None
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))
        
    def check_element_in_list(self, deleted_log_instructions, removed_code):
        try:
            for i, log_instruction in enumerate(deleted_log_instructions):
                cleaned_instruction = log_instruction.instruction.replace("  ", "")
                if cleaned_instruction == removed_code:
                    return i
            return None
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))

    def get_repos(self, repoPath):
        try:
            folder_names = []
            for folder in os.scandir(repoPath):
                if folder.is_dir():
                    folder_names.append(folder.name)
            return folder_names
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))
    
    def git_pull(self, repoPath):
        try:
            # Perform a git pull operation on the repository located at repoPath
            repo = Repo(repoPath)
            repo.remotes.origin.pull()
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))

    def deleteRepo(self, path):
        try:
            # Delete the repository directory
            shutil.rmtree(path, onerror=on_rm_error)
            print("Directory deleted successfully.")
            PopupManager.show_error_popup("Alert", "Directory deleted successfully.")
        except FileNotFoundError:
            traceback.print_exc()
            print("Directory not found.")
            PopupManager.show_error_popup("Alert", "Directory not found.")
        except OSError as e:
            print(f"An error occurred while deleting the directory: {str(e)}")
            traceback.print_exc()
            PopupManager.show_error_popup("Alert", f"An error occurred while deleting the directory: {str(e)}")

    def get_branches(self, repoPath):
        try:
            result = []
            # Get the current branch of the repository
            if os.path.exists(repoPath + ".git"):
                repo = Repo(repoPath)
                result = [str(ref) for ref in repo.refs]
            return result
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))

def on_rm_error(func, path, exc_info):
    try:
        # This function is called when an error occurs while removing a file or directory.
        # It is used to handle read-only files by changing their permissions before unlinking them.
        # The path parameter contains the path of the file or directory that couldn't be removed.
        
        # Change the file or directory permissions to allow write access
        os.chmod(path, stat.S_IWRITE)
        # Unlink (remove) the file or directory
        os.unlink(path)
    except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))

# Getters
def get_added_log_instructions(self):
    return self.added_log_instructions

def get_deleted_log_instructions(self):
    return self.deleted_log_instructions