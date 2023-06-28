import traceback
from datetime import datetime
from model.GlobalModel import GlobalModel
from model.Instructions import Instructions
from git import Repo
from model.Modification import Modification
from model.LogInstruction import LogInstruction
from urllib.parse import urlparse

import shutil
import os
import stat

from view.PopupView import PopupManager

class HomeModel:

    def get_log_instructions(self, repo_url, from_date, to_date, searched_path, searched_branch, searched_author, framework):
            added_log_instructions = []  # Initialize an empty list to store the added log instructions
            deleted_log_instructions = []  # Initialize an empty list to store the deleted log instructions
            
            # Convert the input dates to datetime objects
            from_date_obj = datetime.strptime(from_date, '%Y-%m-%d')
            to_date_obj = datetime.strptime(to_date, '%Y-%m-%d')

            # Create datetime objects for the start and end dates
            dt1 = datetime(from_date_obj.year, from_date_obj.month, from_date_obj.day)
            dt2 = datetime(to_date_obj.year, to_date_obj.month, to_date_obj.day)
            instruction = Instructions(searched_path, [dt1, dt2], [framework], [])
            gm = GlobalModel()
            
            gm.addRepoBranch(repo_url, searched_branch, instruction)
            repoBranch = gm.getRepoBranch(repo_url, searched_branch)
            for key, value in  repoBranch.logs.items():
                if value is not None:
                    for log in value:
                        if(log is not None):
                            if log.modifications[len(log.modifications) - 1].type == 'deleted':
                                deleted_log_instructions.append(log)
                                value.remove(log)
                            else:
                                added_log_instructions.append(log)

            # Save the lists as properties
            self.added_log_instructions = added_log_instructions
            self.deleted_log_instructions = deleted_log_instructions

            
            # Return the list of log instructions that match the criteria
            return self.added_log_instructions, self.deleted_log_instructions, repoBranch.commits, repoBranch.logs

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
            shutil.rmtree(path, onerror=self.on_rm_error)
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

    def on_rm_error(self, func, path, exc_info):
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