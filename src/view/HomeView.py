from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QCalendarWidget, QHBoxLayout, QComboBox
from PyQt6.QtCore import QDate
from view.PopupView import PopupManager

class HomeView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home")
        self.setGeometry(100, 100, 280, 80)
        self.setMaximumSize(280, 80)

        # Create a layout for the widget
        layout = QVBoxLayout(self)

        #Create the search label
        searchLabel = QLabel("Please enter the repository")
        layout.addWidget(searchLabel)

        # Create allow the user to look for present repositories
        self.repoList = QComboBox(self)
        layout.addWidget(self.repoList)

        # Create the buttons for the repositories
        layoutForRepoButton = QHBoxLayout()
        self.newRepoButton = QPushButton("new")
        self.deleteRepoButton = QPushButton("delete")
        layoutForRepoButton.addWidget(self.newRepoButton)
        layoutForRepoButton.addWidget(self.deleteRepoButton)
        layout.addLayout(layoutForRepoButton)

        # Widget pour afficher les dates sélectionnées
        self.from_date_label = QLabel("FROM: ")
        layout.addWidget(self.from_date_label)

        # Calendrier pour la date de début
        self.from_calendar = QCalendarWidget(self)
        layout.addWidget(self.from_calendar)

        self.to_date_label = QLabel("TO: ")
        layout.addWidget(self.to_date_label)

        # Calendrier pour la date de fin
        self.to_calendar = QCalendarWidget(self)
        self.to_calendar.setSelectedDate(QDate.currentDate())  # Sélectionne la date actuelle
        layout.addWidget(self.to_calendar)

        self.setLayout(layout)

        # Create the search button
        self.searchButton = QPushButton("Search")
        layout.addWidget(self.searchButton)
        self.show()

    def setRepos(self, repos):
        self.repos = repos
        for repo in repos:
            self.repoList.addItem(repo)