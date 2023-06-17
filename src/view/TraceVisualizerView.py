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

    def __init__(self, added_log_instructions, deleted_log_instructions):
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
            date_list = [log.date for log in added_log_instructions]
            modif_list = [len(log.modifications) for log in added_log_instructions]

            sns.scatterplot(x=date_list, y=modif_list)
            
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
        

    def set_plot(self, axes, log_instructions_added, log_instructions_deleted):
        try:
            # Créer des listes pour stocker les dates et les nombres de modifications
            dates_added = []
            num_modifications_added = []

            # Parcourir les log_instructions_added
            for log_added in log_instructions_added:
                for modification in log_added.modifications:
                    dates_added.append(modification.get_date())
                    num_modifications_added.append(len(log_added.modifications))
                    
            # for log_deleted in log_instructions_deleted:
            #     for modification in log_deleted.modifications:
            #         dates_added.append(modification.get_date())
            #         num_modifications_added.append(len(log_deleted.modifications))

            # Créer le graphique en utilisant les dates et les nombres de modifications
            axes.plot(dates_added, num_modifications_added, 'o', markersize=4)

            # Ajouter des traits pour montrer la modification d'une instruction à travers plusieurs commits
            for log_instruction in log_instructions_added:
                if len(log_instruction.modifications) > 1:
                    dates = [modification.get_date() for modification in log_instruction.modifications]
                    num_modifications = [len(log_instruction.modifications)] * len(dates)
                    axes.plot(dates, num_modifications, '-', linewidth=0.5, color='gray')

            axes.set_xlabel('Date')
            axes.set_ylabel('Modified instructions')
            axes.set_title('Commit History')
            axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            axes.xaxis.set_major_locator(mdates.DayLocator())
            
            axes.set_xticks(dates_added)
           # axes.set_xticklabels([date.strftime('%Y-%m-%d') for date in dates_added], rotation=90, ha='right')
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))
