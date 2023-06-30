from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QHBoxLayout, QGridLayout, QTabWidget, QComboBox, QSplitter, QFrame, QListWidgetItem
from PyQt6 import QtCore,QtWidgets
from view.PopupView import PopupManager
import matplotlib.dates as mdates
import traceback

class TraceVisualizerView(QWidget):

    def __init__(self):
        try:
            super().__init__()
            self.setWindowTitle("Trace Visualizer")
            self.setGeometry(100, 100, 800, 600)

            self_layout = QHBoxLayout(self)

            # Left Layout
            left_frame = QFrame()
            upper_left_layout = QVBoxLayout(left_frame)
            self.log_instructions_list = QListWidget()
            upper_left_layout.addWidget(QLabel("log instructions"))  # Add the label to the layout
            upper_left_layout.addWidget(self.log_instructions_list)

            # Right Layout
            right_frame = QFrame()
            right_layout = QVBoxLayout(right_frame)
            filters_label = QLabel("Filters")
            filters_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
            filters = QComboBox()
            filters.addItems(["All", "Added", "Deleted", "Modified"])
            
            # plot
            sns.set(style="whitegrid")
            plt.figure(figsize=(10, 6))
            sns.set_theme()
            commitsInfo = self.extractCommitsInfo(added_log_instructions)
            dates = [commit["date"] for commit in commitsInfo]
            index = self.enumerate(dates)
            # logsCount = [commit["logsCount"] for commit in commitsInfo]
            sns.scatterplot(x=dates, y=index)
            plt.legend(["Commit"])
            plt.xlabel("Commit's date")
            plt.ylabel("Logs Count")
            
            right_layout.addWidget(filters_label)
            right_layout.addWidget(filters)
            right_layout.addWidget(plt.gcf().canvas)

            splitter_vertical = QSplitter(QtCore.Qt.Orientation.Vertical)
            splitter_vertical.addWidget(right_frame)

            splitter = QSplitter(QtCore.Qt.Orientation.Horizontal)
            splitter.addWidget(left_frame)
            splitter.addWidget(right_frame)

            self_layout.addWidget(splitter)
            
            self.show()  # Show the widget
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_info_popup("Caught Error", str(e))    

    def set_log_instructions(self, log_instructions):
        try:
            if log_instructions is None:
                raise ValueError("log_instructions cannot be None")
            for log_instruction in log_instructions:
                # Add each commit information as an item to the QListWidget
                if(log_instruction.instruction is not None):
                    item = QListWidgetItem(log_instruction.instruction)
                    item.setData(QtCore.Qt.ItemDataRole.UserRole, log_instruction)
                    self.log_instructions_list.addItem(item)
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_info_popup("Caught Error", str(e))

    def set_graphic(self, graphic):
        if graphic is None:
            raise ValueError("graphic cannot be None")
        # Remove existing graphic from right_layout if it's not None
        if self.graphic is not None:
            self.right_layout.removeWidget(self.graphic)

        # Set the new graphic
        self.graphic = graphic

        # Add the new graphic to right_layout
        self.right_layout.addWidget(self.graphic)


