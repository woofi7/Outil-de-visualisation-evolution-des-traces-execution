from pydriller import Repository
from PyQt6.QtCore import QDate, Qt
from datetime import datetime
from git import Repo
import shutil
import os
import stat

SEARCHED_STRING = ["always","catching", "critical", "debug", "error", "fatal", "info", "warn", "trace", "log", "trace"]
SEARCHED_FILES = ['.java', '.py']

class HomeModel:
    def get_log_instructions(self, repo_url, from_date, to_date):
        result = []  # Initialize an empty list to store the result
        
        # Convert the input dates to datetime objects
        from_date_obj = datetime.strptime(from_date, '%Y-%m-%d')
        to_date_obj = datetime.strptime(to_date, '%Y-%m-%d')
        
        # Create datetime objects for the start and end dates
        dt1 = datetime(from_date_obj.year, from_date_obj.month, from_date_obj.day)
        dt2 = datetime(to_date_obj.year, to_date_obj.month, to_date_obj.day)

        for commit in Repository(repo_url, since=dt1, to=dt2,only_modifications_with_file_types=SEARCHED_FILES).traverse_commits():
            # Traverse through the commits in the repository
            for modification in commit.modified_files:
                added_good_modification_bool, added_good_modification = self.__locate_log_instructions(modification.diff_parsed["added"], SEARCHED_STRING)
                removed_good_modification_bool, removed_good_modification = self.__locate_log_instructions(modification.diff_parsed["deleted"], SEARCHED_STRING)
                if(added_good_modification_bool):
                    print(added_good_modification)
                elif (removed_good_modification_bool):
                    print(removed_good_modification)
        
        return result  # Return the list of commits that match the criteria
    
    def __locate_log_instructions(self, modifications_list, target_strings):
        my_tuple = None
        for t in modifications_list:
            if isinstance(t, tuple) and any(element in t for element in target_strings):
                my_tuple = t
                break
        if my_tuple:
            bool = True
            return bool, my_tuple
        else:
            bool = False
            return bool, None

    def get_repos(self, repoPath):
        folder_names = []
        for folder in os.scandir(repoPath):
            if folder.is_dir():
                folder_names.append(folder.name)
        return folder_names
    
    def git_pull(self, repoPath):
        # Perform a git pull operation on the repository located at repoPath
        repo = Repo(repoPath)
        repo.remotes.origin.pull()

    def deleteRepo(self, path):
        try:
            # Delete the repository directory
            shutil.rmtree(path, onerror=on_rm_error)
            print("Directory deleted successfully.")
        except FileNotFoundError:
            print("Directory not found.")
        except OSError as e:
            print(f"An error occurred while deleting the directory: {str(e)}")

def on_rm_error(func, path, exc_info):
    # This function is called when an error occurs while removing a file or directory.
    # It is used to handle read-only files by changing their permissions before unlinking them.
    # The path parameter contains the path of the file or directory that couldn't be removed.
    
    # Change the file or directory permissions to allow write access
    os.chmod(path, stat.S_IWRITE)
    # Unlink (remove) the file or directory
    os.unlink(path)
