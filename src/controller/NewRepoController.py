import traceback
from view.PopupView import PopupManager
from model.ReposManager import ReposManager
from view.NewRepoView import NewRepoView

class NewRepoController:
    def __init__(self, home_view):
        self.new_repo_view = NewRepoView()
        self.home_view = home_view
        self.repo_manager = ReposManager()
        self.new_repo_view.okButton.clicked.connect(self._ok_button_clicked)
        self.new_repo_view.cancelButton.clicked.connect(self._cancel_button_clicked)

    def _ok_button_clicked(self):
        try:
            # Get the repository name and convert it to path
            repo_name = self.new_repo_view.newRepo.text().split("/")[-1].split(".")[0]
            repo_path = "./repo/" + repo_name + "/"

            # Clone the repository using the model
            self.repo_manager.clone_repo(self.new_repo_view.newRepo.text(), repo_path)

            # Close the current view
            self.new_repo_view.close()

            # Update the repository list in the home controller
            self.home_view.setRepos(self.repo_manager.get_repos("./repo/"))
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_info_popup("Caught Error", str(e))

    def _cancel_button_clicked(self):
        #Close the current view
        self.new_repo_view.close()