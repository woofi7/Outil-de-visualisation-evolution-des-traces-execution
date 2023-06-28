from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QHBoxLayout, QGridLayout, QTabWidget, QComboBox, QSplitter, QFrame, QListWidgetItem
from PyQt6 import QtCore,QtWidgets
import sys
from model.Modification import Modification
# import matplotlib
from view.PopupView import PopupManager
import seaborn as sns
import matplotlib.pyplot as plt

import matplotlib.dates as mdates
from datetime import datetime
from model.LogInstruction import LogInstruction
import traceback

class TraceVisualizerView(QWidget):

    def __init__(self, added_log_instructions, deleted_log_instructions, commits, logs):
        try:
            super().__init__()
            self.setWindowTitle("Trace Visualizer")
            self.setGeometry(100, 100, 800, 600)

            self_layout = QHBoxLayout(self)

            # Left Layout
            left_frame = QFrame()
            upper_left_layout = QVBoxLayout(left_frame)
            self.added_commits_list = QListWidget()
            upper_left_layout.addWidget(QLabel("Added log instructions"))  # Add the label to the layout
            upper_left_layout.addWidget(self.added_commits_list)

            self.deleted_commits_list = QListWidget()
            upper_left_layout.addWidget(QLabel("Deleted log instructions"))  # Add the label to the layout
            upper_left_layout.addWidget(self.deleted_commits_list)

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
            PopupManager.show_error_popup("Caught Error", str(e))
        
    

    def set_log_instruction(self, log_instructions_added, log_instructions_deleted):
        try:
            
            for log_instruction_add in log_instructions_added:
                # Add each commit information as an item to the QListWidget
                if(log_instruction_add.instruction is not None):
                    item = QListWidgetItem(log_instruction_add.instruction)
                    item.setData(QtCore.Qt.ItemDataRole.UserRole, log_instruction_add)
                    self.added_commits_list.addItem(item)
            for log_instruction_delete in log_instructions_deleted:
                # Add each commit information as an item to the QListWidget
                if(log_instruction_delete.instruction is not None):
                    item = QListWidgetItem(log_instruction_delete.instruction.replace("  ","") + "\tnumber of time modified : " + str(len(log_instruction_delete.modifications)))
                    item.setData(QtCore.Qt.ItemDataRole.UserRole, log_instruction_delete)
                    self.deleted_commits_list.addItem(item)
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))


    def extractCommitsInfo(self, added_log_instructions):
        commitsInfo = []
        
        
        for log in added_log_instructions:
            for modification in log.modifications:
                if not any(commit["hash"] == modification.hash for commit in commitsInfo):
                    commitsInfo.append({
                        "hash": modification.hash,
                        "date": modification.date,
                        "logsCount": 0
                    })
                else:
                    for commit in commitsInfo:
                        if commit["hash"] == modification.hash:
                            commit["logsCount"] += 1
                            
        return commitsInfo

    def enumerate(self, dates):
        index = []
        for i, _ in enumerate(dates, start=1):
            index.append(i)
        return index