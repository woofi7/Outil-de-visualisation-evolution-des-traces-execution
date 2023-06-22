import traceback
import os
from git import Repo
import git
import shutil
import stat
from view.PopupView import PopupManager

class ReposManager:
        
        def get_repos(self, main_repo_path):
            try:
                folder_names = []
                for folder in os.scandir(main_repo_path):
                    if folder.is_dir():
                        folder_names.append(folder.name)
                return folder_names
            except Exception as e:
                traceback.print_exc()
                PopupManager.show_error_popup("Caught Error", str(e))
    
        def git_pull(self, repoPath):
            try:
                # Perform a git pull operation on the repository located at repoPath
                repo = git.Repo(repoPath)
                repo.remotes.origin.pull()
            except Exception as e:
                traceback.print_exc()
                PopupManager.show_error_popup("Caught Error", str(e))

        def deleteRepo(self, path):
            try:
                # Delete the repository directory
                shutil.rmtree(path, onerror=self.on_rm_error)
                print("Directory deleted successfully.")
                PopupManager.show_info_popup("Alert", "Directory deleted successfully.")
            except FileNotFoundError:
                traceback.print_exc()
                print("Directory not found.")
                PopupManager.show_error_popup("Alert", "Directory not found.")
            except OSError as e:
                print(f"An error occurred while deleting the directory: {str(e)}")
                traceback.print_exc()
                PopupManager.show_error_popup("Alert", f"An error occurred while deleting the directory: {str(e)}")

        def get_branches(self, repo_path):
            try:
                print(repo_path)
                if not os.path.exists(repo_path + ".git"):
                    raise FileNotFoundError(f"Git repository '{repo_path}' not found.")
                # Get the current branch of the repository
                repo = Repo(repo_path)
                return [str(ref) for ref in repo.refs]
            except Exception as e:
                traceback.print_exc()
                PopupManager.show_error_popup("Caught Error", str(e))
        
        def clone_repo(self, repo_url, repo_path):
            if os.path.exists(repo_path):
                raise FileExistsError(f"Repository '{repo_path}' already exists.")
            # Clone the repository from the specified URL to the given path
            Repo.clone_from(repo_url, repo_path)

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