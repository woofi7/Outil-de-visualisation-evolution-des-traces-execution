from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, QLineEdit
from view.PopupView import PopupManager
import traceback

class NewRepoView(QWidget):
    def __init__(self):
        try:
            super().__init__()
            self.setWindowTitle("new repository")
            self.setGeometry(100, 100, 280, 80)

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
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))