from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QListWidget, QTextEdit, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QColor, QTextCursor
from view.PopupView import PopupManager
import traceback

class CommitWindowView(QWidget):
    def __init__(self, commit):
            super().__init__()
            print(commit)
            print(f"commit length : {len(commit[0][:7])}")
            self.setWindowTitle(f"Commit Changes: {commit[0][:7]}")
            print(f"COMMIT HASH : {commit[0][:7]}")
            self.setGeometry(200, 200, 800, 600)
            
            layout = QVBoxLayout()

            label = QLabel(f"Commit: {commit[0][:7]}", self)
            layout.addWidget(label)

            self.code_tables = {}  # Dictionnaire pour stocker les tables de chaque fichierw

            label1 = QLabel(f"File: {commit[1]}\n", self)
            layout.addWidget(label1)

            file_layout = QVBoxLayout()

            self.code_table = QTableWidget(self)
            self.code_table.setColumnCount(2)
            self.code_table.setHorizontalHeaderLabels(["Avant", "Après"])
            self.code_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
                    
            before_lines = commit[2].splitlines() if commit[2] else []
            after_lines = commit[3].splitlines() if commit[3] else []
            max_lines = max(len(before_lines), len(after_lines))

            self.code_table.setRowCount(max_lines)

            for i in range(max_lines):
                before_item = QTableWidgetItem(before_lines[i] if i < len(before_lines) else "")
                after_item = QTableWidgetItem(after_lines[i] if i < len(after_lines) else "")

                self.code_table.setItem(i, 0, before_item)
                self.code_table.setItem(i, 1, after_item)

                self.highlight_code(before_item, QColor(255, 255, 0))  # Couleur jaune pour le code avant
                self.highlight_code(after_item, QColor(0, 255, 0))  # Couleur verte pour le code après

            self.code_table.resizeColumnsToContents()
            self.code_table.resizeRowsToContents()

            layout.addWidget(self.code_table)
            layout.addLayout(file_layout)

            self.setLayout(layout)
            self.show()  # Show the widget


    def highlight_code(self, item, color):
        item.setBackground(color)