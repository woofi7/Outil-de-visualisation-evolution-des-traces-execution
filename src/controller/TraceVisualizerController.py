from view.PopupView import PopupManager
from view.SelectCommitWindowView import SelectCommitWindowView
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
    def __init__(self, frameworks, from_date, to_date, repo_path, searched_path, searched_branch, searched_author):
        try:
            log_instructions = {}
            deleted_instruction = []
            self.trace_visualizer_view = TraceVisualizerView()
            self.log_instruction_diff_generator = LogInstructionDiffGenerator()
            # Connect the searchButton's clicked signal to the search_button_clicked slot
            self.trace_visualizer_view.log_instructions_list.itemClicked.connect(self._show_commit_changes)

            # Retrieve commits based on the selected dates using the model
            for framework in frameworks:
                self.log_instruction_collector = self._set_strategy_collector(framework.text())
                framework_log_instructions, framework_deleted_instruction = self.log_instruction_collector.get_log_instructions(repo_path, from_date, to_date, searched_path, searched_branch, searched_author)
                if(framework_log_instructions and len(framework_log_instructions)):
                    log_instructions.update(framework_log_instructions)
                if(framework_deleted_instruction and len(framework_deleted_instruction)):
                    deleted_instruction.extend(framework_deleted_instruction)
            # Create a new TraceVisualizerView and pass the retrieved commits to it
            self.trace_visualizer_view.set_log_instructions(log_instructions, deleted_instruction)
            self.strategy_generator_file = self._set_strategy_generator_file("csv")
            self.trace_visualizer_view.set_graphic(GraphBuilder().build_graph(self.strategy_generator_file.createFile(log_instructions, deleted_instruction)))
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
            self.CommitWindowView = SelectCommitWindowView(commitChanges)
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_info_popup("Caught Error", str(e))

    def _set_strategy_collector(self, strategy):
        if strategy == "log4p":
            return Log4pCollector()
        elif strategy == "log4j":
            return Log4jCollector()
        else:
            raise ValueError("Invalid strategy name")
        
    def _set_strategy_generator_file(self, strategy):
        if strategy == "csv":
            return CsvFileGenerator()
        else:
            raise ValueError("Invalid strategy name")
