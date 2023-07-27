from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QHBoxLayout, QComboBox, QSplitter, QFrame, QListWidgetItem
from PyQt6 import QtCore,QtWidgets
import matplotlib.pyplot as plt
from view.PopupView import PopupManager

import traceback
import csv


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
            self.log_instructions_list.setMouseTracking(True)
            upper_left_layout.addWidget(QLabel("log instructions"))  # Add the label to the layout
            upper_left_layout.addWidget(self.log_instructions_list)
            
            # Right Layout
            self.graphic = None
            self.right_frame = QFrame()
            self.right_layout = QVBoxLayout(self.right_frame)
            filters_label = QLabel("Filters")
            filters_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
            filters = QComboBox()
            filters.addItems(["All", "Added", "Deleted", "Modified"])
            
            self.right_layout.addWidget(filters_label)
            self.right_layout.addWidget(filters)

            splitter_vertical = QSplitter(QtCore.Qt.Orientation.Vertical)
            splitter_vertical.addWidget(self.right_frame)
            splitter = QSplitter(QtCore.Qt.Orientation.Horizontal)
            splitter.addWidget(left_frame)
            splitter.addWidget(self.right_frame)
            splitter.setStretchFactor(1, 1)
            self_layout.addWidget(splitter)
            
            self.show()  # Show the widget

    def handleResizeEvent(self, event):
        self.resizeGraphic()
        super().resizeEvent(event)

    def set_log_instructions(self, log_instructions):
        try:
            if log_instructions is None:
                raise ValueError("log_instructions cannot be None")

            self.log_instructions_list.clear()
            added_instructions = set()
            def add_log_instruction(log):
                if log.instruction is not None:
                    instruction_key = f"{log.level}, {log.instruction}"
                    item = QListWidgetItem(instruction_key)
                    item.setData(QtCore.Qt.ItemDataRole.UserRole, log)
                    self.log_instructions_list.addItem(item)
                    added_instructions.add(instruction_key)

            for log in log_instructions:
                add_log_instruction(log)

        except Exception as e:
            traceback.print_exc()
            PopupManager.show_info_popup("Caught Error", str(e))

    def set_graphic(self, graphic):
        if graphic is None:
            raise ValueError("graphic cannot be None")

        # Remove existing graphic from right_layout if it's not None
        if self.graphic is not None:
            plt.close(self.graphic.figure)
            old_frame = self.graphic.parentWidget()
            self.right_layout.removeWidget(old_frame)
            old_frame.setParent(None)

        # Set the new graphic
        self.graphic = graphic

        # Create a new QFrame to contain the graphic
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.addWidget(self.graphic)

        # Add the new frame to right_layout
        self.right_layout.addWidget(frame)
        
        # Highlight the log instructions
        self.graphic.mpl_connect('motion_notify_event', lambda event: self.highlight_log(event, self.log_instructions_list))

    def resizeGraphic(self):
        # Retrieve the size of the QFrame
        frameSize = self.right_layout.parent().size()

        # Adjust the size of the graphic frame
        self.graphic.parentWidget().resize(frameSize)

        # Adjust the size of the FigureCanvas
        self.graphic.setGeometry(0, 0, frameSize.width(), frameSize.height())

        # Redraw the canvas
        self.graphic.draw()

    def highlight_log(self, event, log_instructions_list):
        if event.inaxes:
            x, y = event.xdata, event.ydata
            # x_after, y_after = event.x, event.y
            # x_date = mdates.num2date(x)
            
            # print(str(y))
            # print(str(x_date))

            # Find the corresponding row in the table
                    # print("IN: ", y)
            log_instructions_list.setCurrentRow(round(y)-1)
                # else:
                #     print("OUT: ", y)
                #     log_instructions_list.clearSelection()
                
    def get_instruction_for_index(self, index):
        closerInt = round(index)
        
        if abs(index - closerInt) <=0.2:
            index = closerInt
        else:
            return None
        
        with open('../csv/data.csv', 'r') as file:
            csv_data = csv.reader(file)
            next(csv_data)
            for row in csv_data:
                if row[0] == str(index):
                    return row[1]

        return None
