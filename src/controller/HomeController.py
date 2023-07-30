from view.NewRepoView import NewRepoView
from controller.NewRepoController import NewRepoController
from view.PopupView import PopupManager
from view.TraceVisualizerView import TraceVisualizerView
from controller.TraceVisualizerController import TraceVisualizerController
from model.ReposManager import ReposManager
from datetime import datetime
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QFileDialog
from functools import partial
from view.HomeView import HomeView
import traceback

REPO_FOLDER = "./repo/"

class HomeController:
    def __init__(self):
        self.home_view = HomeView()
        self.repos_manager = ReposManager()
        self.home_view.setRepos(self.repos_manager.get_repos(REPO_FOLDER))
        self._update_branch_list(self.home_view.repoList.currentText())

        # Connect button click events to corresponding functions
        self.home_view.newRepoButton.clicked.connect(partial(self._new_repo_button_clicked))
        self.home_view.searchButton.clicked.connect(self._search_button_clicked)
        self.home_view.from_calendar.selectionChanged.connect(self._validate_date_range)
        self.home_view.to_calendar.selectionChanged.connect(self._validate_date_range)
        self.home_view.deleteRepoButton.clicked.connect(self._delete_repo_button_clicked)
        self.home_view.repoList.currentTextChanged.connect(self._update_branch_list)
        self.home_view.load_from_csv_button.clicked.connect(self.load_csv_file)

    def _search_button_clicked(self):
            # Retrieve selected dates and repository name from the view
            from_date = datetime.strptime(self.home_view.from_calendar.selectedDate().toString(Qt.DateFormat.ISODate), '%Y-%m-%d')
            to_date = datetime.strptime(self.home_view.to_calendar.selectedDate().toString(Qt.DateFormat.ISODate), '%Y-%m-%d')
            repo_path = REPO_FOLDER + self.home_view.repoList.currentText() + "/"

            searched_path = self.home_view.searched_path.text()
            searched_branch = self.home_view.branches.currentText()
            searched_author = self.home_view.searched_author.text()
            frameworks = self.home_view.slected_framework.selectedItems()

            # Perform a Git pull in the repository
            self.repos_manager.git_pull(repo_path)

            # Create a new TraceVisualizerView and pass the retrieved commits to it
            self.trace_visualizer_controller = TraceVisualizerController(frameworks, from_date, to_date, repo_path, searched_path, searched_branch, searched_author)
            # Close the current view
            self.home_view.close()

    def _validate_date_range(self):
        from_date = self.home_view.from_calendar.selectedDate()
        self.home_view.from_date_label.setText("FROM: " + from_date.toString())
        to_date = self.home_view.to_calendar.selectedDate()
        self.home_view.to_date_label.setText("TO: " + to_date.toString()) 

        if from_date > to_date:
            self.home_view.popupError("Invalid Date Range", "La date 'FROM' ne peut pas être postérieure à la date 'TO'.")
        else:
            print("Valid date range")

    def _update_branch_list(self, repo_name):
        if repo_name.strip():
                repo_path = REPO_FOLDER + self.home_view.repoList.currentText() + "/"
                self.home_view.setBranches(self.repos_manager.get_branches(repo_path))

    def _new_repo_button_clicked(self):
            self.new_repo_controller = NewRepoController(self.home_view)

    def _delete_repo_button_clicked(self):
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

    def load_csv_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self.home_view, "Load CSV File", "", "CSV Files (*.csv);;All Files (*)", options=QFileDialog.Option.ReadOnly)
        # if file_name:
        #     self.show_csv_file_info(file_name)