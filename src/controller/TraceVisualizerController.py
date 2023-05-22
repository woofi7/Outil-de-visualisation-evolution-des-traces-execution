from view.HomeView import HomeView
# from model.HomeModel import HomeModel
from view.TraceVisualizerView import TraceVisualizerView
from view.CommitWindowView import CommitWindowView

class TraceVisualizerController:
    def __init__(self, view, model, home_view):
        self.view = view
        self.model = model
        self.home_view = home_view
        # Connect the searchButton's clicked signal to the search_button_clicked slot
        self.view.trace_list.itemClicked.connect(self.show_commit_changes)

    def show_commit_changes(self, item):
        commit_hash = item.text().split(", File: ")[0].split(": ")[1]
        commitChanges = self.model.getCommitChanges(commit_hash, self.home_view.searchInput.text())
        # Create a new TraceVisualizerView and pass the retrieved commits to it
        self.CommitWindowView = CommitWindowView(commitChanges)

        self.view.commit_windows.append(self.CommitWindowView)