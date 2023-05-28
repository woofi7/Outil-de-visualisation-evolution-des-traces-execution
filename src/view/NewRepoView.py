from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, QLineEdit

class NewRepoView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("new repository")
        self.setGeometry(100, 100, 280, 80)
        self.setMaximumSize(280, 80)

        # Create a layout for the widget
        layout = QGridLayout(self)

        #Create the search label
        searchLabel = QLabel("Please enter the repository")
        layout.addWidget(searchLabel)

        # Create allow the user to look for present repositories
        self.newRepo = QLineEdit(self)
        layout.addWidget(self.newRepo)

        # Create the buttons for the repositories
        self.okButton = QPushButton("ok")
        self.cancelButton = QPushButton("cancel")
        layout.addWidget(self.okButton)
        layout.addWidget(self.cancelButton)
        self.show()