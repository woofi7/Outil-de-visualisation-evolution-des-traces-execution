from view.PopupView import PopupManager
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QCalendarWidget, QHBoxLayout, QComboBox, QLineEdit
from PyQt6.QtCore import QDate
import traceback

class HomeView(QWidget):
    def __init__(self):
        try:
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

            layout.addWidget(QLabel("Please enter the path in the repository ex: src\model (leave empty for all)"))
            self.searched_path = QLineEdit()
            layout.addWidget(self.searched_path)

            layout.addWidget(QLabel("Please enter the branch in the repository"))
            self.branches = QComboBox()
            layout.addWidget(self.branches)

            layout.addWidget(QLabel("Please enter the author of the commits (leave empty for all)"))
            self.searched_author = QLineEdit()
            layout.addWidget(self.searched_author)

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
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))

    def setRepos(self, repos):
        try: 
            self.repos = repos
            for repo in repos:
                self.repoList.addItem(repo)
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))

    def setBranches(self, branches):

        try:
            for branch in branches:
                self.branches.addItem(branch)
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))
    def popupError(self,title,  message):
       PopupManager.show_error_popup(title, message)
