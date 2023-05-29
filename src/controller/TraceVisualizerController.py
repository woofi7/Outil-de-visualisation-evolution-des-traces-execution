from view.HomeView import HomeView
from view.TraceVisualizerView import TraceVisualizerView
from view.CommitWindowView import CommitWindowView

REPO_FOLDER = "./repo/"

class TraceVisualizerController:
    def __init__(self, view, model, home_view):
        self.view = view
        self.model = model
        self.home_view = home_view

        # Connect the searchButton's clicked signal to the search_button_clicked slot
        self.view.commits_list.itemClicked.connect(self.show_commit_changes)

    def show_commit_changes(self, item):
        # Extract the commit hash from the clicked item
        commit_hash = item.text().split(", File: ")[0].split(": ")[1]

        # Get the current selected repository name from the home view
        repo_name = self.home_view.repoList.currentText()

        # Construct the repository path
        repo_path = REPO_FOLDER + repo_name + "/"

        # Retrieve the commit changes using the model
        commitChanges = self.model.getCommitChanges(commit_hash, repo_path)

        # Create a new CommitWindowView and pass the retrieved commit changes to it
        self.CommitWindowView = CommitWindowView(commitChanges)

        # Append the CommitWindowView to the view's commit_windows list
        self.view.commit_windows.append(self.CommitWindowView)
