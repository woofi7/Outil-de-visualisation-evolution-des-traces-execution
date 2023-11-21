import os

import git
from view.PopupView import PopupManager
from controller.TraceVisualizerController import TraceVisualizerController
from model.ReposManager import ReposManager
from datetime import datetime
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog
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

        self.home_view.openButton.clicked.connect(self._open_file_dialog)
        self.home_view.cloneButton.clicked.connect(self._clone_repo)

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
            self.trace_visualizer_controller = TraceVisualizerController.fromArgs(frameworks, from_date, to_date, repo_path, searched_path, searched_branch, searched_author)
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
        pass
    
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
        file_name, _ = QFileDialog.getOpenFileName(self.home_view, "Load File", "./files", "JSON Files (*.json);;All Files (*)", options=QFileDialog.Option.ReadOnly)
        print("File name: " + file_name)
        self.trace_visualizer_controller = TraceVisualizerController.fromFile(file_name)
        self.home_view.close()

    def _clone_repo(self):
        try:
            if os.path.isdir(self.home_view.cloneRepo.text()):
                local_project_path = self.home_view.cloneRepo.text()
                local_repo = git.Repo(local_project_path)
                remote_url = local_repo.remotes.origin.url
            else:
                remote_url = self.home_view.cloneRepo.text()

            repo_name = remote_url.split("/")[-1].split(".")[0]
            repo_path = "./repo/" + repo_name + "/"

            # Clone the repository using the model
            self.repos_manager.clone_repo(remote_url, repo_path)

            # Clear the text
            self.home_view.cloneRepo.clear()

            # Update the repository list in the home controller
            self.home_view.setRepos(self.repos_manager.get_repos("./repo/"))
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_info_popup("Caught Error", str(e))

    def _open_file_dialog(self):
        folder_path = QFileDialog.getExistingDirectory()
        if folder_path:
            self.home_view.cloneRepo.setText(folder_path)