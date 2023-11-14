from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QListWidget, QTextEdit, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QColor, QTextCursor
from view.PopupView import PopupManager
import traceback
import difflib

class CommitWindowView(QWidget):
    diff_removed = QColor(200, 130, 130)
    diff_added = QColor(130, 200, 130)
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
                if len(before_lines) == 0 or after_lines == 0:
                    before_item = QTableWidgetItem(before_lines[i] if i < len(before_lines) else "")
                    after_item = QTableWidgetItem(after_lines[i] if i < len(after_lines) else "")

                    self.code_table.setItem(i, 0, before_item)
                    self.code_table.setItem(i, 1, after_item)


                    self.highlight_code(before_item, self.diff_removed)  # Couleur jaune pour le code avant
                    self.highlight_code(after_item, self.diff_added)  # Couleur verte pour le code après
                else:
                    diff = list(difflib.ndiff(before_lines,after_lines))
                    for i in range(max(len(before_lines), len(after_lines))):
                        before_item = QTableWidgetItem(before_lines[i] if i < len(before_lines) else "")
                        after_item = QTableWidgetItem(after_lines[i] if i < len(after_lines) else "")

                        self.code_table.setItem(i, 0, before_item)
                        self.code_table.setItem(i, 1, after_item)

                        # Check if the line is in the diff
                        if ('- ' + before_lines[i]) in diff or ('+ ' + after_lines[i]) in diff:
                            self.highlight_code(before_item, self.diff_removed)  # Yellow for the code before
                            self.highlight_code(after_item, self.diff_added)


            self.code_table.resizeColumnsToContents()
            self.code_table.resizeRowsToContents()

            layout.addWidget(self.code_table)
            layout.addLayout(file_layout)

            self.setLayout(layout)
            self.show()  # Show the widget


    def highlight_code(self, item, color):
        item.setBackground(color)