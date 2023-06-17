from model.DataModel import DataModel

class GlobalModel:
    def __init__(self):
        self.repos = dict(dict())

    
    # Get the dictionnary of branches and dataModels from a repo
    def getRepo(self, repo):
        if(repo in self.repos):
            return self.repos[repo]
        else:
            raise ValueError("Aucun repo avec ce nom n'existe.")
    
    # Get the datamodel of a branch from a repo
    def getRepoBranch(self, repo, branch):
        if(repo in self.repos):
            if(branch in self.repos[repo]):
                return self.repos[repo].get(branch)
            raise ValueError("Aucune branche avec ce nom n'existe.")
        raise ValueError("Aucun repo avec ce nom n'existe.")
    
    # Add a branch to a repo, add also the repo if not already there
    def addRepoBranch(self, repo, branch, instructions):
        if repo in self.repos:
            if branch in self.repos[repo]:
                raise ValueError("Une branche avec le même nom existe déjà pour ce repo.")
            self.repos[repo][branch] = DataModel(repo, branch, instructions)
        else:
            self.repos[repo] = {branch: DataModel(repo, branch, instructions)}
    
    # Remove a repo with all its branches and dataModels
    def removeRepo(self, repo):
        if repo in self.repos:
            del self.repos[repo]
        else:
            raise ValueError("Aucun repo avec ce nom n'existe.")
    
    # Remove a branch and dataModel from a repo
    def removeRepoBranch(self, repo, branch):
        if repo in self.repos:
            if branch in self.repos[repo]:
                del self.repos[repo][branch]
            else:
                raise ValueError("Aucune branche avec ce nom n'existe.")
        else:
            raise ValueError("Aucun repo avec ce nom n'existe.")