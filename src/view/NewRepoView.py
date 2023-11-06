from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, QLineEdit, QFrame, QFileDialog
from view.PopupView import PopupManager
import traceback


class NewRepoView(QWidget):
    def __init__(self):
        try:
            super().__init__()
            self.setWindowTitle("New Repository")
            self.setGeometry(100, 100, 280, 80)

            layout = QGridLayout(self)

            # Clone remote
            layout.addWidget(QLabel("Clone an external repository"))
            self.cloneRepo = QLineEdit(self)
            layout.addWidget(self.cloneRepo)

            # Open local
            layout.addWidget(QLabel("Open a local repository"))
            self.openRepo = QLineEdit(self)
            self.openButton = QPushButton("Select Folder")
            layout.addWidget(self.openRepo)
            layout.addWidget(self.openButton)

            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)  # This creates a horizontal line
            line.setFrameShadow(QFrame.Shadow.Sunken)
            layout.addWidget(line)

            self.cloneButton = QPushButton("Clone")
            layout.addWidget(self.cloneButton)
            self.cancelButton = QPushButton("Cancel")
            layout.addWidget(self.cancelButton)

            self.show()
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_info_popup("Caught Error", str(e))