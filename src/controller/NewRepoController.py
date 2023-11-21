import traceback

import git
import os
from PyQt6.QtWidgets import QFileDialog

from view.PopupView import PopupManager
from model.ReposManager import ReposManager
from view.NewRepoView import NewRepoView


class NewRepoController:
    def __init__(self, home_view):
        self.new_repo_view = NewRepoView()
        self.home_view = home_view
        self.repo_manager = ReposManager()
        self.new_repo_view.openButton.clicked.connect(self._open_file_dialog)

        self.new_repo_view.cloneButton.clicked.connect(self._clone_repo)
        self.new_repo_view.cancelButton.clicked.connect(self._cancel_button_clicked)

    def _clone_repo(self):
        try:
            if os.path.isdir(self.new_repo_view.cloneRepo.text()):
                local_project_path = self.new_repo_view.cloneRepo.text()
                local_repo = git.Repo(local_project_path)
                remote_url = local_repo.remotes.origin.url
            else:
                remote_url = self.new_repo_view.cloneRepo.text()

            repo_name = remote_url.split("/")[-1].split(".")[0]
            repo_path = "./repo/" + repo_name + "/"

            # Clone the repository using the model
            self.repo_manager.clone_repo(remote_url, repo_path)

            # Close the current view
            self.new_repo_view.close()

            # Update the repository list in the home controller
            self.home_view.setRepos(self.repo_manager.get_repos("./repo/"))
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_info_popup("Caught Error", str(e))

    def _cancel_button_clicked(self):
        self.new_repo_view.close()

    def _open_file_dialog(self):
        folder_path = QFileDialog.getExistingDirectory()
        if folder_path:
            self.new_repo_view.cloneRepo.setText(folder_path)
