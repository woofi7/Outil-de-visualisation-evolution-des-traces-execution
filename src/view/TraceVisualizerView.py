from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QTextEdit

class TraceVisualizerView(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trace Visualizer")
        self.setGeometry(100, 100, 800, 600)
        self.setMaximumSize(800, 600)
        layout = QVBoxLayout()

        label = QLabel("Hello, Trace Visualizer!", self)
        layout.addWidget(label)

        self.trace_list = QListWidget(self)
        layout.addWidget(self.trace_list)

        code_display = QTextEdit(self)
        layout.addWidget(code_display)
        self.show()