from view.HomeView import HomeView
from model.HomeModel import HomeModel
from view.TraceVisualizerView import TraceVisualizerView

class HomeController():
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.view.searchButton.clicked.connect(self.search_button_clicked)

    def search_button_clicked(self):
        searchText = self.view.searchInput.text()
        self.model.getCommits(searchText)
        self.view.close()
        self.traceVisualizerView = TraceVisualizerView()
