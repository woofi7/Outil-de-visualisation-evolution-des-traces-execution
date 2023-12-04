from model.LogInstructionsFileGenerators.JsonFileGenerator import JsonFileGenerator
from view.PopupView import PopupManager
from view.SelectCommitWindowView import SelectCommitWindowView
from view.TraceVisualizerView import TraceVisualizerView
from model.LogInstructionDiffGenerator import LogInstructionDiffGenerator
from model.LogInstructionCollectors.LogInstruction import LogInstruction
from model.GraphBuilders.GraphManager import GraphManager
from model.LogInstructionCollectors.Log4pCollector import Log4pCollector
from model.LogInstructionCollectors.Log4jCollector import Log4jCollector
from model.LogInstructionsFileGenerators.CsvFileGenerator import CsvFileGenerator
from PyQt6 import QtCore
from PyQt6.QtWidgets import QFileDialog, QMessageBox
import json
import traceback

REPO_FOLDER = "./repo/"

class TraceVisualizerController:
    annotationFilters = GraphManager._annotation_filters
    log_instruction_collector = None

    def __init__(self, all_log_instructions):


        try:
            self.all_log_instructions = all_log_instructions
            self.trace_visualizer_view = TraceVisualizerView()
            self.log_instruction_diff_generator = LogInstructionDiffGenerator()

            # Setup the view
            self.filtered_log_instructions = self.all_log_instructions
            self._set_view_data(self.all_log_instructions)
            
            # Connect the searchButton's clicked signal to the search_button_clicked slot
            self.trace_visualizer_view.log_instructions_list.itemClicked.connect(self._show_commit_changes)
            
            # Connect the data from the list to the graph
            self.trace_visualizer_view.log_instructions_list.itemEntered.connect(self._highlight_graph_element)
            
            # Connect to save data button
            self.trace_visualizer_view.save_data_button.clicked.connect(self._save_data)
            
            # Connect to go back to home
            self.trace_visualizer_view.home_button.clicked.connect(self._navigate_to_home)

            for checkbox in self.annotationFilters:
                self.trace_visualizer_view._checkboxes[checkbox].stateChanged.connect(self._checkbox_state_changed)

            # Connect the filters to the data
            filterWidget = self.trace_visualizer_view.right_layout.itemAt(1).widget()
            filterWidget.currentTextChanged.connect(lambda: self._filter_logs(filterWidget))
            
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_info_popup("Caught Error", str(e))

    def _checkbox_state_changed(self,state):
        # 2 is the checked state for a checkbox
        if state is 2:
            self.annotationFilters.append(self.trace_visualizer_view.sender().text())
        else:
            self.annotationFilters.remove(self.trace_visualizer_view.sender().text())
        GraphManager().set_annotation_filters(self.annotationFilters)
    @classmethod
    def fromArgs(cls, frameworks, from_date, to_date, repo_path, searched_path, searched_branch, searched_author):
        try:
            all_log_instructions = []

            cls.from_date = from_date
            cls.to_date = to_date
            # Retrieve commits based on the selected dates using the model
            for framework in frameworks:
                cls.log_instruction_collector = cls._set_strategy_collector(framework.text())
                framework_logs = cls.log_instruction_collector.get_log_instructions(repo_path, searched_path, searched_branch, searched_author)
                all_log_instructions.extend(framework_logs)
                
            return cls(all_log_instructions)
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_info_popup("Caught Error", str(e))
            
    @classmethod
    def fromFile(cls, file_path):
        try:
            all_log_instructions = []
            
            with open(file_path, 'r') as f:
                data = json.load(f)
                all_log_instructions = [LogInstruction.from_dict(d) for d in data]
            
            return cls(all_log_instructions)
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_info_popup("Caught Error", str(e))

    def _show_commit_changes(self, item):
        try:
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

    def _set_strategy_collector(strategy):
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
        
    def _set_view_data(self, log_instructions):
        self.trace_visualizer_view.set_log_instructions(log_instructions)
        self.strategy_generator_file = self._set_strategy_generator_file("csv")
        self.trace_visualizer_view.set_graphic(
            GraphManager().init_graph(
                self.strategy_generator_file.createFile(log_instructions), self.from_date, self.to_date))
        
    def _filter_logs(self, filterWidget):
        types = {"Added": "ModificationType.ADD", "Deleted": "ModificationType.DELETE", "Modified": "ModificationType.MODIFY"}
        filter = filterWidget.currentText()
        filteredLogs = []
        
        for log in self.all_log_instructions:
            filteredLogs.append(log.copy())
        
        if filter == "All":
            pass
        elif filter in types.keys():
            modifType = types[filter]
            for log in filteredLogs[:]:
                for modif in log.modifications[:]:
                    if str(modif.type) != modifType:
                        log.modifications.remove(modif)
                if len(log.modifications) == 0:
                    filteredLogs.remove(log)
        else:
            raise ValueError("Invalid filter value: " + filter)

        GraphManager().set_data(self.strategy_generator_file.createFile(filteredLogs))
        self.filtered_log_instructions = filteredLogs

    def _highlight_graph_element(self, item):
        instruction = self.trace_visualizer_view.log_instructions_list.row(item)
        GraphManager().set_highlighted_instruction(instruction)
        
    def _save_data(self):
        file_name, _ = QFileDialog.getSaveFileName(self.trace_visualizer_view, "Save File", "./files", "JSON Files (*.json);;All Files (*)")
        jsonGenerator = JsonFileGenerator()
        jsonGenerator.createFile(self.all_log_instructions, file_name)
        
        msg = QMessageBox()
        msg.setWindowTitle("File saved")
        msg.setText(file_name + " has been saved.")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()

    def _navigate_to_home(self):
        from controller.HomeController import HomeController
        self.trace_visualizer_view.close()
        HomeController()

    def update_view(self, frameworks, from_date, to_date, repo_path, searched_path, searched_branch, searched_author):
        try:
            all_log_instructions = []

            # Retrieve commits based on the selected dates using the model
            for framework in frameworks:
                self.log_instruction_collector = self._set_strategy_collector(framework.text())
                framework_logs = self.log_instruction_collector.get_log_instructions(repo_path, searched_path, searched_branch, searched_author)
                all_log_instructions.extend(framework_logs)

            # Update the existing view with the new log instructions
            self.all_log_instructions = all_log_instructions
            self._set_view_data(all_log_instructions)

        except Exception as e:
            traceback.print_exc()
            PopupManager.show_info_popup("Caught Error", str(e))