from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QHBoxLayout, QGridLayout, QTabWidget, QComboBox
from PyQt6 import QtCore,QtWidgets
import sys
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class TraceVisualizerView(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trace Visualizer")
        self.setGeometry(100, 100, 800, 600)
        self.setMaximumSize(800, 600)

        self_layout = QHBoxLayout(self)
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        self_layout.addLayout(left_layout)
        self_layout.addLayout(right_layout)

        # Left Layout
        label = QLabel("Current log instructions")  # Create a label widget
        self.commits_list = QListWidget()
        left_layout.addWidget(label)  # Add the label to the layout
        left_layout.addWidget(self.commits_list)

        # Right Layout
        filters_label = QLabel("Filters")
        filters = QComboBox()
        filters.addItems(["All", "Added", "Deleted", "Modified"])
        right_layout.addWidget(filters_label)
        right_layout.addWidget(filters)

        # Plot
        canvas, axes = self._create_plot(6, 6, 100)
        axes.plot([0,1,2,3,4], [10,1,20,3,40])
        toolbar = NavigationToolbar(canvas)
        right_layout.addWidget(toolbar)
        right_layout.addWidget(canvas)

        self.show()  # Show the widget

    def _create_plot(self,width, height, dpi):
        fig = Figure(figsize=(width, height), dpi=dpi)
        axes = fig.add_subplot(111)
        canvas = FigureCanvasQTAgg(fig)
        return canvas, axes
        

    def setCommits(self, commits):
        for commit in commits:
            # Add each commit information as an item to the QListWidget
            self.commits_list.addItem(f"Commit: {commit[0]}, File: {commit[1]}, "
                f"Added Lines: {commit[2]}, Deleted Lines: {commit[3]}")
