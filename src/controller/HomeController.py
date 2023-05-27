from view.HomeView import HomeView
from model.HomeModel import HomeModel
from view.TraceVisualizerView import TraceVisualizerView
from model.TraceVisualizerModel import TraceVisualizerModel
from controller.TraceVisualizerController import TraceVisualizerController
from PyQt6.QtCore import QDate, Qt

class HomeController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        # Connect the searchButton's clicked signal to the search_button_clicked slot
        self.view.searchButton.clicked.connect(self.search_button_clicked)
        self.view.from_calendar.selectionChanged.connect(self.update_from_date)
        self.view.to_calendar.selectionChanged.connect(self.update_to_date)
        #self.view.select_button.clicked.connect(self.on_select_button_clicked)

    def search_button_clicked(self):
        searchText = self.view.searchInput.text()  # Get the search input text from the view
        from_date = self.view.from_calendar.selectedDate().toString(Qt.DateFormat.ISODate)
        to_date = self.view.to_calendar.selectedDate().toString(Qt.DateFormat.ISODate)
        print(from_date)
        print(to_date)
        repoName = searchText.split("/")[-1].split(".")[0]
        repoPath = "../repo/" + repoName
        self.model.cloneRepo(searchText,repoPath)  # Clone the repository using the model
        commits = self.model.getCommits(repoPath, from_date, to_date)  # Retrieve commits based on the search text using the model
        self.view.close()  # Close the current view

        # Create a new TraceVisualizerView and pass the retrieved commits to it
        self.traceVisualizerView = TraceVisualizerView(commits)
        self.traceVisualizerModel = TraceVisualizerModel()
        self.traceVisualizerController = TraceVisualizerController(self.traceVisualizerView, self.traceVisualizerModel, self.view)

    def update_from_date(self):
        from_date = self.view.from_calendar.selectedDate()
        self.view.from_date_label.setText("FROM: " + from_date.toString())

    def update_to_date(self):
        to_date = self.view.to_calendar.selectedDate()
        self.view.to_date_label.setText("TO: " + to_date.toString())    