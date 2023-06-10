from view.NewRepoView import NewRepoView
from model.NewRepoModel import NewRepoModel
from controller.NewRepoController import NewRepoController
from view.PopupView import PopupManager
from view.TraceVisualizerView import TraceVisualizerView
from model.TraceVisualizerModel import TraceVisualizerModel
from controller.TraceVisualizerController import TraceVisualizerController
from PyQt6.QtCore import QDate, Qt
import os
import traceback

REPO_FOLDER = "./repo/"

class HomeController:
    def __init__(self, view, model):
        try:
            self.view = view
            self.model = model
            self.update_repo_list()
            self.update_branch_list()

            # Connect button click events to corresponding functions
            self.view.newRepoButton.clicked.connect(self.new_repo_button_clicked)
            self.view.searchButton.clicked.connect(self.search_button_clicked)
            self.view.from_calendar.selectionChanged.connect(self.validate_date_range)
            self.view.to_calendar.selectionChanged.connect(self.validate_date_range)
            self.view.deleteRepoButton.clicked.connect(self.delete_repo_button_clicked)
            self.view.repoList.currentTextChanged.connect(self.update_branch_list)
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))

    def search_button_clicked(self):
        try:
            # Retrieve selected dates and repository name from the view
            from_date = self.view.from_calendar.selectedDate().toString(Qt.DateFormat.ISODate)
            to_date = self.view.to_calendar.selectedDate().toString(Qt.DateFormat.ISODate)
            repoName = self.view.repoList.currentText()
            repoPath = REPO_FOLDER + repoName + "/"

            searched_path = self.view.searched_path.text()
            if searched_path is None:
                searched_path = ""
            searched_branch = self.view.branches.currentText()
            searched_author = self.view.searched_author.text()
            if searched_author is None:
                searched_author = ""

            # Perform a Git pull in the repository
            self.model.git_pull(repoPath)

            # Retrieve commits based on the selected dates using the model
            added_log_instructions, deleted_log_instructions = self.model.get_log_instructions(repoPath, from_date, to_date, searched_path, searched_branch, searched_author)

            # Close the current view
            self.view.close()

            # Create a new TraceVisualizerView and pass the retrieved commits to it
            self.traceVisualizerView = TraceVisualizerView(added_log_instructions, deleted_log_instructions)
            self.traceVisualizerView.set_log_instruction(added_log_instructions, deleted_log_instructions)
            self.traceVisualizerModel = TraceVisualizerModel()
            self.traceVisualizerController = TraceVisualizerController(self.traceVisualizerView, self.traceVisualizerModel, self.view, self.model)
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))

    def validate_date_range(self):
      
        try:
            from_date = self.view.from_calendar.selectedDate()
            self.update_from_date()
            to_date = self.view.to_calendar.selectedDate()
            self.update_to_date()

            if from_date > to_date:
                self.view.popupError("Invalid Date Range", "La date 'FROM' ne peut pas être postérieure à la date 'TO'.")
            else:
                print("Valid date range")
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))

    def update_from_date(self):
        try:
            # Update the "FROM" date label based on the selected date
            from_date = self.view.from_calendar.selectedDate()
            self.view.from_date_label.setText("FROM: " + from_date.toString())
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))

    def update_to_date(self):
        try:
            # Update the "TO" date label based on the selected date
            to_date = self.view.to_calendar.selectedDate()
            self.view.to_date_label.setText("TO: " + to_date.toString()) 
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))

    def new_repo_button_clicked(self):
        try:
            # Create a new repository view, model, and controller
            self.NewRepoView = NewRepoView()
            self.NewRepoModel = NewRepoModel()
            self.NewRepoController = NewRepoController(self.NewRepoView, self.NewRepoModel, self)
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))

    def update_repo_list(self):
        try:
            # Clear the repository list and set the repositories in the view
            self.create_directory(REPO_FOLDER)
            self.view.repoList.clear()
            self.view.setRepos(self.model.get_repos(REPO_FOLDER))
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))

    def update_branch_list(self):
        try:
            self.view.branches.clear()
            repoName = self.view.repoList.currentText()
            repoPath = REPO_FOLDER + repoName + "/"
            self.view.setBranches(self.model.get_branches(repoPath))
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))

    def delete_repo_button_clicked(self):
        try:
            # Retrieve the selected repository name from the view
            repoName = self.view.repoList.currentText()
            repoPath = REPO_FOLDER + repoName + "/"

            # Delete the repository using the model
            self.model.deleteRepo(repoPath)

            # Update the repository list in the view
            self.update_repo_list()
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))
    
    def create_directory(self, directory_path):
        try:
            # Create a directory if it doesn't exist
            if not os.path.exists(directory_path):
                try:
                    os.makedirs(directory_path)
                except OSError as e:
                    print(f"An error occurred while creating the directory: {str(e)}")
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))
