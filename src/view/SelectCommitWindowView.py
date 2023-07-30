from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QListWidget, QTextEdit, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QListWidgetItem
from PyQt6.QtGui import QColor, QTextCursor
from view.PopupView import PopupManager
from view.CommitWindowView import CommitWindowView
from PyQt6.QtCore import Qt 
import traceback
class SelectCommitWindowView(QWidget):
    def __init__(self, commit_changes):
        super().__init__()
        self.setWindowTitle("Select Commit")
        self.setGeometry(200, 200, 400, 300)
        
        layout = QVBoxLayout()
        label = QLabel("Select a commit:", self)
        layout.addWidget(label)
        self.commit_list = QListWidget(self)
        layout.addWidget(self.commit_list)

        for commit in commit_changes:
            item = QListWidgetItem(commit[0][:7] + " by " + commit[4], self.commit_list)
            item.setData(Qt.ItemDataRole.UserRole, commit)  # Store the complete commit

        select_button = QPushButton("Select", self)
        layout.addWidget(select_button)
        select_button.clicked.connect(self.handleSelect)
        self.setLayout(layout)
        self.show()
    
    def handleSelect(self):
        selected_item = self.commit_list.currentItem()
        if selected_item:
            selected_commit = selected_item.data(Qt.ItemDataRole.UserRole)  # Get the complete commit
            #self.close()
            self.commit_window = CommitWindowView(selected_commit)
            #commit_window.show()