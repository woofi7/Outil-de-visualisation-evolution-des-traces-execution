from git import Repo
import os

class NewRepoModel:
    def cloneRepo(self, repoUrl, repoPath):
        # Check if the repository path exists
        if not os.path.exists(repoPath):
            # Clone the repository from the specified URL to the given path
            Repo.clone_from(repoUrl, repoPath)
