from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QListWidget, QTextEdit, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QColor, QTextCursor

class CommitWindowView(QWidget):
    def __init__(self, commit_changes):
        super().__init__()
        #print(commit_changes[0][0])
        commit_hash = commit_changes[0][0]
        self.setWindowTitle(f"Commit Changes: {commit_hash}")
        self.setGeometry(200, 200, 800, 600)
        
        layout = QVBoxLayout()

        label = QLabel(f"Commit: {commit_hash}", self)
        layout.addWidget(label)

        # AUTEUR ET DATE WIP
        # author_label = QLabel(f"Auteur: {commit.author.name}", self)
        # layout.addWidget(author_label)

        # date_label = QLabel(f"Date: {commit.author_date}", self)
        # layout.addWidget(date_label)

        # self.file_buttons = {}  # Dictionnaire pour stocker les boutons de chaque fichier
        self.code_tables = {}  # Dictionnaire pour stocker les tables de chaque fichierw

        for commit in commit_changes:
            label1 = QLabel(f"File: {commit[1]}\n", self)
            layout.addWidget(label1)

            file_layout = QVBoxLayout()

        #     # show_hide_button = QPushButton("Show", self)
        #     # file_layout.addWidget(show_hide_button)
        #     # show_hide_button.setCheckable(True)
        #     # show_hide_button.setChecked(False)
                    
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

        #     # self.file_buttons[commit[1]] = show_hide_button
        #     self.code_tables[commit[1]] = self.code_table


            layout.addWidget(self.code_table)
            layout.addLayout(file_layout)

        #     #show_hide_button.clicked.connect(lambda checked, name=commit_changes[1]: self.toggle_code_table(checked, name))

        # widget = QWidget()
        self.setLayout(layout)
        # self.setCentralWidget(self)
        self.show()  # Show the widget

    # def toggle_code_table(self, checked, filename):
    #     table = self.code_tables.get(filename)
    #     if table:
    #         if checked:
    #             table.show()
    #         else:
    #             table.hide()

    def highlight_code(self, item, color):
        item.setBackground(color)