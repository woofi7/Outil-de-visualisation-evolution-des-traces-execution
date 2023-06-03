from view.HomeView import HomeView
from view.PopupView import PopupManager
from view.TraceVisualizerView import TraceVisualizerView
from view.CommitWindowView import CommitWindowView
from PyQt6 import QtCore
import traceback

REPO_FOLDER = "./repo/"

class TraceVisualizerController:
    def __init__(self, view, model, home_view):
        try:
            self.view = view
            self.model = model
            self.home_view = home_view

            # Connect the searchButton's clicked signal to the search_button_clicked slot
            #self.view.commits_list.itemClicked.connect(self.show_commit_changes)
            self.view.added_commits_list.itemClicked.connect(self.show_commit_changes)
            self.view.deleted_commits_list.itemClicked.connect(self.show_commit_changes)
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))

    def show_commit_changes(self, item):
        try:
            print('ITEM : ')
            print(item.data(QtCore.Qt.ItemDataRole.UserRole).modifications)
            commits = []
            modifications = item.data(QtCore.Qt.ItemDataRole.UserRole).modifications
            for modification in modifications:
                print(modification.commit.hash)
                commits.append(modification.commit)


            # Extract the commit hash from the clicked item
            # commit_hash = item.text().split(", File: ")[0].split(": ")[1]

            # # Get the current selected repository name from the home view
            # repo_name = self.home_view.repoList.currentText()

            # # Construct the repository path
            # repo_path = REPO_FOLDER + repo_name + "/"

            # Retrieve the commit changes using the model
            # commitChanges = self.model.getCommitChanges(commit_hash, repo_path)
            commitChanges = self.model.getCommitChanges(commits)

            #print(commitChanges)

            # Create a new CommitWindowView and pass the retrieved commit changes to it
            self.CommitWindowView = CommitWindowView(commitChanges)

            # Append the CommitWindowView to the view's commit_windows list
            #self.view.commit_windows.append(self.CommitWindowView)
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))
