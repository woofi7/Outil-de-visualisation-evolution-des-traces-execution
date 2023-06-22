from view.HomeView import HomeView
from view.PopupView import PopupManager
from model.LogInstructionDiffGenerator import LogInstructionDiffGenerator
from view.CommitWindowView import CommitWindowView
from PyQt6 import QtCore
import traceback

REPO_FOLDER = "./repo/"

class TraceVisualizerController:
    def __init__(self, trace_visualiser_view):
        try:
            self.trace_visualiser_view = trace_visualiser_view
            self.trace_visualizer_model = LogInstructionDiffGenerator()

            # Connect the searchButton's clicked signal to the search_button_clicked slot
            self.trace_visualiser_view.log_instructions_list.itemClicked.connect(self.show_commit_changes)
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_info_popup("Caught Error", str(e))

    def show_commit_changes(self, item):
        try:
            print('ITEM : ')
            print(item.data(QtCore.Qt.ItemDataRole.UserRole).modifications)
            commits = []
            modifications = item.data(QtCore.Qt.ItemDataRole.UserRole).modifications
            for modification in modifications:
                commits.append(modification)

            commitChanges = self.trace_visualizer_model.getCommitChanges(commits)

            # Create a new CommitWindowView and pass the retrieved commit changes to it
            self.CommitWindowView = CommitWindowView(commitChanges)
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_info_popup("Caught Error", str(e))
