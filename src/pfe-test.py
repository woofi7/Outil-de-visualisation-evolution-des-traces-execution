import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QListWidget, QTextEdit
from pydriller import Repository

class TraceVisualizer(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trace Visualizer")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        label = QLabel("Hello, Trace Visualizer!", self)
        layout.addWidget(label)

        self.trace_list = QListWidget(self)
        layout.addWidget(self.trace_list)

        code_display = QTextEdit(self)
        layout.addWidget(code_display)

        repo_url = 'https://github.com/Projet-de-fin-etudes/Outil-de-visualisation-evolution-des-traces-execution'
        for commit in Repository(repo_url).traverse_commits():
            for modification in commit.modified_files:
                self.trace_list.addItem(f"Commit: {commit.hash[:7]}, File: {modification.filename}, "
                                   f"Added Lines: {modification.added_lines}, Deleted Lines: {modification.deleted_lines}")

        # trace_list.itemClicked.connect(lambda item: self.show_code(item.text(), code_display))
        self.trace_list.itemClicked.connect(self.show_commit_changes)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.commit_windows = []  # Liste pour stocker les instances de CommitWindow

    def show_commit_changes(self, item):
        commit_hash = item.text().split(", File: ")[0].split(": ")[1]
        print(commit_hash)
        commit_window = CommitWindow(commit_hash)
        commit_window.show()
        self.commit_windows.append(commit_window)  # Ajout de l'instance à la liste

class CommitWindow(QMainWindow):
    def __init__(self, commit_hash):
        super().__init__()
        self.setWindowTitle(f"Commit Changes: {commit_hash}")
        self.setGeometry(200, 200, 800, 600)
        self.initUI(commit_hash)

    def initUI(self, commit_hash):
        layout = QVBoxLayout()

        label = QLabel(f"Commit: {commit_hash}", self)
        layout.addWidget(label)

        code_display = QTextEdit(self)
        layout.addWidget(code_display)

        repo_url = 'https://github.com/Projet-de-fin-etudes/Outil-de-visualisation-evolution-des-traces-execution'
        for commit in Repository(repo_url).traverse_commits():
            #print(commit.hash.startswith(commit_hash))
            if commit.hash.startswith(commit_hash):
                for modification in commit.modified_files:
                    code_display.append(f"File: {modification.filename}\n")
                    code_display.append("Before:\n")
                    code_display.append(modification.source_code_before)
                    code_display.append("\nAfter:\n")
                    code_display.append(modification.source_code)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TraceVisualizer()
    window.show()
    sys.exit(app.exec())
