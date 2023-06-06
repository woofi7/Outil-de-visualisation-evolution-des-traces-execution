import traceback
from pydriller import Repository

from view.PopupView import PopupManager

class DataModel:
    def __init__(self, repo, branch, instructions):
        self.repo = repo
        self.branch = branch
        self.instructions = instructions
        self.commits = []
        
        try:
            for commit in Repository(repo, since=instructions.dates[0], to=instructions.dates[1], only_modifications_with_file_types=instructions.fileTypes, only_in_branch=branch).traverse_commits():
                if(instructions.authors==[] or commit.author in instructions.authors):
                    self.commits.append(commit)
                    for modification in commit.modified_files:
                        if any(modification.filename.endswith(ext) for ext in instructions.fileTypes) and any(path in modification.old_path for path in instructions.paths) and any(path in modification.new_path for path in instructions.paths):
                            print("jsuis rendu ici...")
        
        
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))

        
        
        
    # Fonction pour comparer 2 objets DataModel
    def __eq__(self, other):
        if isinstance(other, DataModel):
            return self.repo == other.repo and self.branch == other.branch
        return False