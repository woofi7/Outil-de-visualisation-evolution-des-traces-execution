class NewRepoController:
    def __init__(self, newRepoView, newRepomodel, homeController):
        self.view = newRepoView
        self.model = newRepomodel
        self.view.okButton.clicked.connect(self.ok_button_clicked)
        self.view.cancelButton.clicked.connect(self.cancel_button_clicked)
        self.homeController = homeController

    def ok_button_clicked(self):
        # Get the repository name and path from the view
        repoName = self.view.newRepo.text().split("/")[-1].split(".")[0]
        repoPath = "./repo/" + repoName + "/"

        # Clone the repository using the model
        self.model.cloneRepo(self.view.newRepo.text(), repoPath)

        # Close the current view
        self.view.close()

        # Update the repository list in the home controller
        self.homeController.update_repo_list()

    def cancel_button_clicked(self):
        # Close the current view
        self.view.close()