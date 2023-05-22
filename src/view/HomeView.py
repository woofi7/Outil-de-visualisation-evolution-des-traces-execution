from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QCalendarWidget

class HomeView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home")
        self.setGeometry(100, 100, 280, 80)
        self.setMaximumSize(280, 80)

        # Create a layout for the widget
        layout = QVBoxLayout(self)

        #Create the search label
        searchLabel = QLabel("Please enter the repository URL")
        layout.addWidget(searchLabel)

        # Create the search input field
        self.searchInput = QLineEdit()
        layout.addWidget(self.searchInput)

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
        layout.addWidget(self.to_calendar)

        # Bouton pour sélectionner les dates
        self.select_button = QPushButton("Select Dates")
        #select_button.clicked.connect(self.on_select_button_clicked)
        layout.addWidget(self.select_button)

        self.setLayout(layout)

        # Create the search button
        self.searchButton = QPushButton("Search")
        layout.addWidget(self.searchButton)
        self.show()