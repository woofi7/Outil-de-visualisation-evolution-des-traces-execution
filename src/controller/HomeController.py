from view.HomeView import HomeView
from model.HomeModel import HomeModel
from view.TraceVisualizerView import TraceVisualizerView

class HomeController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        # Connect the searchButton's clicked signal to the search_button_clicked slot
        self.view.searchButton.clicked.connect(self.search_button_clicked)

    def search_button_clicked(self):
        searchText = self.view.searchInput.text()  # Get the search input text from the view
        commits = self.model.getCommits(searchText)  # Retrieve commits based on the search text using the model
        self.view.close()  # Close the current view

        # Create a new TraceVisualizerView and pass the retrieved commits to it
        self.traceVisualizerView = TraceVisualizerView(commits)
