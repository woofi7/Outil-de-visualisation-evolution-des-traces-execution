import traceback
from view.PopupView import PopupManager

class NewRepoController:
    def __init__(self, newRepoView, newRepomodel, homeController):
        try:
            self.view = newRepoView
            self.model = newRepomodel
            self.view.okButton.clicked.connect(self.ok_button_clicked)
            self.view.cancelButton.clicked.connect(self.cancel_button_clicked)
            self.homeController = homeController
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))    

    def ok_button_clicked(self):
        try:
            # Get the repository name and path from the view
            repoName = self.view.newRepo.text().split("/")[-1].split(".")[0]
            repoPath = "./repo/" + repoName + "/"

            # Clone the repository using the model
            self.model.cloneRepo(self.view.newRepo.text(), repoPath)

            # Close the current view
            self.view.close()

            # Update the repository list in the home controller
            self.homeController.update_repo_list()
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))

    def cancel_button_clicked(self):
        # Close the current view
        self.view.close()