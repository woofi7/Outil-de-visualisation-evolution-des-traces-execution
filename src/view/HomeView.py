from view.PopupView import PopupManager
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QCalendarWidget, QHBoxLayout, QComboBox, \
    QLineEdit, QListWidget, QPushButton, QFrame
from PyQt6.QtCore import QDate
import traceback

class HomeView(QWidget):
    def __init__(self):
        try:
            super().__init__()
            self.setWindowTitle("Home")
            self.setGeometry(100, 100, 280, 80)

            # Create a layout for the widget
            layout = QVBoxLayout(self)

            # Clone remote
            layout.addWidget(QLabel("Clone an external or local repository"))
            self.cloneRepo = QLineEdit(self)
            layout.addWidget(self.cloneRepo)

            self.openButton = QPushButton("Select Folder")
            layout.addWidget(self.openButton)

            self.cloneButton = QPushButton("Clone")
            layout.addWidget(self.cloneButton)

            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)  # This creates a horizontal line
            line.setFrameShadow(QFrame.Shadow.Sunken)
            layout.addWidget(line)

            #Create the search label
            searchLabel = QLabel("Please select a repository")
            layout.addWidget(searchLabel)

            # Create allow the user to look for present repositories
            self.repoList = QComboBox(self)
            layout.addWidget(self.repoList)

            self.slected_framework = QListWidget()
            self.slected_framework.setSelectionMode(QListWidget.SelectionMode.MultiSelection)


            # Create the buttons for the repositories
            layoutForRepoButton = QHBoxLayout()
            self.newRepoButton = QPushButton("new")
            self.deleteRepoButton = QPushButton("delete")
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

            layout.addWidget(QLabel("Please enter the logging framework you want to analyse"))

            layout.addWidget(self.slected_framework)

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

            # Create the "Load from csv" button
            self.load_from_csv_button = QPushButton("Load from file", self)
            layout.addWidget(self.load_from_csv_button)

            self.show()
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_info_popup("Caught Error", str(e))

    def setRepos(self, repos):
        try: 
            self.repoList.clear()
            for repo in repos:
                self.repoList.addItem(repo)
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_info_popup("Caught Error", str(e))

    def setBranches(self, branches):
        try:
            self.branches.clear()
            for branch in branches:
                self.branches.addItem(branch)
        except Exception as e:
            #traceback.print_exc()
            PopupManager.show_info_popup("Caught Error", str(e))

    # def load_csv_file(self):
    #     file_name, _ = QFileDialog.getOpenFileName(self, "Load CSV File", "", "CSV Files (*.csv);;All Files (*)", options=QFileDialog.Option.ReadOnly)
    #     # if file_name:
    #     #     self.show_csv_file_info(file_name)
    
    def popupError(self,title,  message):
       PopupManager.show_info_popup(title, message)


