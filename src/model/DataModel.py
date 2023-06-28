import traceback
from pydriller import Repository

from view.PopupView import PopupManager

class DataModel:
    def __init__(self, repo, branch, instructions):
        self.repo = repo
        self.branch = branch
        self.instructions = instructions
        self.commits = []
        self.logs = {}
        
        try:
            # filter commits by repo, dates, file types and branch
            for commit in Repository(repo, only_modifications_with_file_types=instructions.fileTypes, only_in_branch=branch).traverse_commits():
                # filter commits by authors
                if commit.hash == "af8ae057f1ab2e25a2ffefcb0d061c4f530582bc":
                    print("woohoo")
                if(instructions.authors==[] or commit.author in instructions.authors):
                    self.commits.append(commit)
                    for modified_file in commit.modified_files:
                        self.logs[modified_file.filename] = []
                        # filter files by file types and paths
                        if any(modified_file.filename.endswith(ext) for ext in instructions.fileTypes) and ((modified_file.old_path is not None and instructions.paths in modified_file.old_path) or (modified_file.new_path is not None and instructions.paths in modified_file.new_path)):
                            # filter logs by framework
                            for strategy in instructions.frameworkStrategies:
                                if modified_file.filename == "test_StrategyLog4p.py":
                                    print("woohoo")
                                self.logs[modified_file.filename] = strategy.getLogs(commit.hash, modified_file.filename, modified_file.source_code_before, modified_file.source_code, commit.committer_date, self.logs[modified_file.filename])
                        # if self.logs[modified_file.filename] == None or len(self.logs[modified_file.filename]) == 0:
                        #     del self.logs[modified_file.filename]
        
            print("allo")
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))

        
    # Function to compare two DataModels
    def __eq__(self, other):
        if isinstance(other, DataModel):
            return self.repo == other.repo and self.branch == other.branch
        return False