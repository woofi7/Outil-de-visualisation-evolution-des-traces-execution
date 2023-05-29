from pydriller import Repository
from PyQt6.QtCore import QDate, Qt
from datetime import datetime
from git import Repo
import shutil
import os
import stat

SEARCHED_STRING = ["always","catching", "critical", "debug", "error", "fatal", "info", "warn", "trace", "log", "trace"]

class HomeModel:
    def getCommits(self, repo_url, from_date, to_date):
        result = []  # Initialize an empty list to store the result
        
        # Convert the input dates to datetime objects
        from_date_obj = datetime.strptime(from_date, '%Y-%m-%d')
        to_date_obj = datetime.strptime(to_date, '%Y-%m-%d')
        
        # Create datetime objects for the start and end dates
        dt1 = datetime(from_date_obj.year, from_date_obj.month, from_date_obj.day)
        dt2 = datetime(to_date_obj.year, to_date_obj.month, to_date_obj.day)

        for commit in Repository(repo_url, since=dt1, to=dt2, order='reverse').traverse_commits():
            # Traverse through the commits in the repository
            for modification in commit.modified_files:
                # Iterate over the modified files in each commit
                if modification.source_code is not None and any(word in modification.source_code for word in SEARCHED_STRING):
                    # If the searched string is found, add the commit details to the result list
                    result.append([commit.hash[:7], modification.filename, modification.added_lines, modification.deleted_lines])
        
        return result  # Return the list of commits that match the criteria

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
