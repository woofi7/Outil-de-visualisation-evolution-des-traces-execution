from pydriller import Repository

SEARCHED_STRING = "LOG4J"

class TraceVisualizerModel:
    def getCommitChanges(self, commit_hash, repo_url):
        result = []  # Initialize an empty list to store the result
        for commit in Repository(repo_url).traverse_commits():
            if commit.hash.startswith(commit_hash):
                for modification in commit.modified_files:
                    result.append([commit.hash[:7], modification.filename, modification.source_code_before, modification.source_code])
        return result  # Return the list of commits that match the criteria