from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel

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

        # Create the search button
        self.searchButton = QPushButton("Search")
        layout.addWidget(self.searchButton)
        self.show()