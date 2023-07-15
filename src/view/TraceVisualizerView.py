from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QHBoxLayout, QGridLayout, QTabWidget, QComboBox, QSplitter, QFrame, QListWidgetItem
from PyQt6 import QtCore,QtWidgets
from view.PopupView import PopupManager
import matplotlib.dates as mdates
import traceback

class TraceVisualizerView(QWidget):

    def __init__(self):
            super().__init__()
            self.setWindowTitle("Trace Visualizer")
            self.setGeometry(100, 100, 1000, 800)

            self_layout = QHBoxLayout(self)

            # Left Layout
            left_frame = QFrame()
            upper_left_layout = QVBoxLayout(left_frame)
            self.log_instructions_list = QListWidget()
            upper_left_layout.addWidget(QLabel("log instructions"))  # Add the label to the layout
            upper_left_layout.addWidget(self.log_instructions_list)

            # Right Layout
            self.graphic = None
            right_frame = QFrame()
            self.right_layout = QVBoxLayout(right_frame)
            filters_label = QLabel("Filters")
            filters_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
            filters = QComboBox()
            filters.addItems(["All", "Added", "Deleted", "Modified"])
            
            self.right_layout.addWidget(filters_label)
            self.right_layout.addWidget(filters)

            splitter_vertical = QSplitter(QtCore.Qt.Orientation.Vertical)
            splitter_vertical.addWidget(right_frame)
            splitter = QSplitter(QtCore.Qt.Orientation.Horizontal)
            splitter.addWidget(left_frame)
            splitter.addWidget(right_frame)
            splitter.setStretchFactor(1, 1)
            self_layout.addWidget(splitter)
            
            self.show()  # Show the widget

    def set_log_instructions(self, log_instructions, deleted_instruction):
            if log_instructions is None:
                raise ValueError("log_instructions cannot be None")
            for log_instruction, value in log_instructions.items():
                if value is not None:
                    for log in value:
                    # Add each commit information as an item to the QListWidget
                        if(log.instruction is not None):
                            item = QListWidgetItem(f"{log.level}, {log.instruction}")
                            item.setData(QtCore.Qt.ItemDataRole.UserRole, log)
                            self.log_instructions_list.addItem(item)

            for value in deleted_instruction:
                if value is not None:
                    # Add each commit information as an item to the QListWidget
                        if(value.instruction is not None):
                            item = QListWidgetItem(f"{log.level}, {log.instruction}")
                            item.setData(QtCore.Qt.ItemDataRole.UserRole, log)
                            self.log_instructions_list.addItem(item)

    def set_graphic(self, graphic):
        if graphic is None:
            raise ValueError("graphic cannot be None")
        # Remove existing graphic from right_layout if it's not None
        if self.graphic is not None:
            self.right_layout.removeWidget(self.graphic)

        # Set the new graphic
        graphic.setGeometry(0, 0, self.right_layout.sizeHint().width(), self.right_layout.sizeHint().height())
        self.graphic = graphic

        # Add the new graphic to right_layout
        self.right_layout.addWidget(self.graphic)


