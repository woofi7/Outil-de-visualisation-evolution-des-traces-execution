from view.PopupView import PopupManager
from view.TraceVisualizerView import TraceVisualizerView
from view.CommitWindowView import CommitWindowView
from model.LogInstructionDiffGenerator import LogInstructionDiffGenerator
from model.GraphBuilders.GraphBuilder import GraphBuilder
from model.LogInstructionCollectors.Log4pCollector import Log4pCollector
from model.LogInstructionCollectors.Log4jCollector import Log4jCollector
from model.LogInstructionsFileGenerators.CsvFileGenerator import CsvFileGenerator
from PyQt6 import QtCore
import traceback

REPO_FOLDER = "./repo/"

class TraceVisualizerController:
    def __init__(self, framework, from_date, to_date, repo_path, searched_path, searched_branch, searched_author):
        try:
            self.trace_visualizer_view = TraceVisualizerView()
            self.log_instruction_diff_generator = LogInstructionDiffGenerator()
            # Connect the searchButton's clicked signal to the search_button_clicked slot
            self.trace_visualizer_view.log_instructions_list.itemClicked.connect(self._show_commit_changes)

            # Retrieve commits based on the selected dates using the model
            self.log_instruction_collector = self._set_strategy(framework)
            log_instructions = self.log_instruction_collector.get_log_instructions(repo_path, from_date, to_date, searched_path, searched_branch, searched_author)

            # Create a new TraceVisualizerView and pass the retrieved commits to it
            self.trace_visualizer_view.set_log_instructions(log_instructions)
            self.trace_visualizer_view.set_graphic(GraphBuilder().build_graph(CsvFileGenerator().createFile(log_instructions)))
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_info_popup("Caught Error", str(e))

    def _show_commit_changes(self, item):
        try:
            print('ITEM : ')
            print(item.data(QtCore.Qt.ItemDataRole.UserRole).modifications)
            commits = []
            modifications = item.data(QtCore.Qt.ItemDataRole.UserRole).modifications
            for modification in modifications:
                commits.append(modification)
            commitChanges = self.log_instruction_diff_generator.getCommitChanges(commits)

            # Create a new CommitWindowView and pass the retrieved commit changes to it
            self.CommitWindowView = CommitWindowView(commitChanges)
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_info_popup("Caught Error", str(e))

    def _set_strategy(self, strategy):
        if strategy == "log4p":
            return Log4pCollector()
        elif strategy == "log4j":
            return Log4jCollector()
        else:
            raise ValueError("Invalid strategy name")
