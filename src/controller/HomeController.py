from view.NewRepoView import NewRepoView
from controller.NewRepoController import NewRepoController
from view.PopupView import PopupManager
from view.TraceVisualizerView import TraceVisualizerView
from controller.TraceVisualizerController import TraceVisualizerController
from model.ReposManager import ReposManager
from model.LogInstructionCollectors.LogInstructionCollector import LogInstructionCollector
from model.LogInstructionCollectors.Log4pCollector import Log4pCollector
from model.LogInstructionCollectors.Log4jCollector import Log4jCollector
from datetime import datetime
from PyQt6.QtCore import Qt
from functools import partial


import traceback

REPO_FOLDER = "./repo/"

class HomeController:
    def __init__(self, home_view):
        self.home_view = home_view
        self.repos_manager = ReposManager()
        self.home_view.setRepos(self.repos_manager.get_repos(REPO_FOLDER))
        self._update_branch_list(self.home_view.repoList.currentText())

        # Connect button click events to corresponding functions
        self.home_view.newRepoButton.clicked.connect(partial(self.new_repo_button_clicked))
        self.home_view.searchButton.clicked.connect(self.search_button_clicked)
        self.home_view.from_calendar.selectionChanged.connect(self.validate_date_range)
        self.home_view.to_calendar.selectionChanged.connect(self.validate_date_range)
        self.home_view.deleteRepoButton.clicked.connect(self.delete_repo_button_clicked)
        self.home_view.repoList.currentTextChanged.connect(self._update_branch_list)

    def search_button_clicked(self):
        try:
            # Retrieve selected dates and repository name from the view
            from_date = datetime.strptime(self.home_view.from_calendar.selectedDate().toString(Qt.DateFormat.ISODate), '%Y-%m-%d')
            to_date = datetime.strptime(self.home_view.to_calendar.selectedDate().toString(Qt.DateFormat.ISODate), '%Y-%m-%d')
            repo_path = REPO_FOLDER + self.home_view.repoList.currentText() + "/"

            searched_path = self.home_view.searched_path.text()
            searched_branch = self.home_view.branches.currentText()
            searched_author = self.home_view.searched_author.text()
            framework = self.home_view.slected_framework.currentText()

            # Perform a Git pull in the repository
            self.repos_manager.git_pull(repo_path)

            # Retrieve commits based on the selected dates using the model
            self.log_instruction_collector = self._set_strategy(framework)
            log_instructions = self.log_instruction_collector.get_log_instructions(repo_path, from_date, to_date, searched_path, searched_branch, searched_author)

            # Create a new TraceVisualizerView and pass the retrieved commits to it
            self.traceVisualizerView = TraceVisualizerView()
            self.traceVisualizerView.set_log_instructions(log_instructions)
            self.traceVisualizerController = TraceVisualizerController(self.traceVisualizerView)
            # Close the current view
            self.home_view.close()
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))

    def _set_strategy(self, strategy):
        if strategy == "log4p":
            return Log4pCollector()
        elif strategy == "log4j":
            return Log4jCollector()
        else:
            raise ValueError("Invalid strategy name")

    def validate_date_range(self):
        try:
            from_date = self.home_view.from_calendar.selectedDate()
            self.home_view.from_date_label.setText("FROM: " + from_date.toString())
            to_date = self.home_view.to_calendar.selectedDate()
            self.home_view.to_date_label.setText("TO: " + to_date.toString()) 

            if from_date > to_date:
                self.home_view.popupError("Invalid Date Range", "La date 'FROM' ne peut pas être postérieure à la date 'TO'.")
            else:
                print("Valid date range")
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))

    def _update_branch_list(self, repo_name):
        if repo_name.strip():
                repo_path = REPO_FOLDER + self.home_view.repoList.currentText() + "/"
                self.home_view.setBranches(self.repos_manager.get_branches(repo_path))

    def new_repo_button_clicked(self):
            self.new_repo_view = NewRepoView()
            self.new_repo_controller = NewRepoController(self.new_repo_view, self.home_view)

    def delete_repo_button_clicked(self):
        try:
            repo_name = self.home_view.repoList.currentText()
            repo_path = REPO_FOLDER + repo_name + "/"
            # Delete the repository using the model
            self.repos_manager.deleteRepo(repo_path)
            # Update the repository list in the view
            self.home_view.setRepos(self.repos_manager.get_repos(REPO_FOLDER))
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))