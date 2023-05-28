from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QTextEdit

class TraceVisualizerView(QWidget):

    def __init__(self, commits):
        super().__init__()
        self.setWindowTitle("Trace Visualizer")
        self.setGeometry(100, 100, 800, 600)
        self.setMaximumSize(800, 600)

        layout = QVBoxLayout(self)  # Create a vertical layout for the widget

        label = QLabel("Hello, Trace Visualizer!", self)  # Create a label widget
        layout.addWidget(label)  # Add the label to the layout

        self.trace_list = QListWidget(self)  # Create a QListWidget widget
        layout.addWidget(self.trace_list)  # Add the QListWidget to the layout

        # code_display = QTextEdit(self)  # Create a QTextEdit widget
        # code_display.setReadOnly(True)  # Set the QTextEdit widget as read-only
        # layout.addWidget(code_display)  # Add the QTextEdit to the layout

        self.commit_windows = []  # Liste pour stocker les instances de CommitWindow

        for commit in commits:
            # Add each commit information as an item to the QListWidget
            self.trace_list.addItem(f"Commit: {commit[0]}, File: {commit[1]}, "
                f"Added Lines: {commit[2]}, Deleted Lines: {commit[3]}")

        self.show()  # Show the widget
