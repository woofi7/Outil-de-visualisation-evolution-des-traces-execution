import traceback
from pydriller import Repository

from view.PopupView import PopupManager

class DataModel:
    def __init__(self, repo, branch, instructions):
        self.repo = repo
        self.branch = branch
        self.instructions = instructions
        self.commits = []
        self.logs = []
        
        try:
            # filter commits by repo, dates, file types and branch
            for commit in Repository(repo, since=instructions.dates[0], to=instructions.dates[1], only_modifications_with_file_types=instructions.fileTypes, only_in_branch=branch).traverse_commits():
                # filter commits by authors
                if(instructions.authors==[] or commit.author in instructions.authors):
                    self.commits.append(commit)
                    for modified_file in commit.modified_files:
                        # filter files by file types and paths
                        if any(modified_file.filename.endswith(ext) for ext in instructions.fileTypes) and any(path in modified_file.old_path for path in instructions.paths) and any(path in modified_file.new_path for path in instructions.paths):
                            # filter logs by framework
                            for strategy in instructions.frameworkStrategies:
                                self.logs.extend(strategy.getLogs(modified_file.source_code_before, modified_file.source_code))
        
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))

        
    # Function to compare two DataModels
    def __eq__(self, other):
        if isinstance(other, DataModel):
            return self.repo == other.repo and self.branch == other.branch
        return False