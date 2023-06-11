from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QHBoxLayout, QGridLayout, QTabWidget, QComboBox, QSplitter, QFrame, QListWidgetItem
from PyQt6 import QtCore,QtWidgets
import sys
import matplotlib
from view.PopupView import PopupManager
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
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
            right_layout.addWidget(filters_label)
            right_layout.addWidget(filters)

            splitter_vertical = QSplitter(QtCore.Qt.Orientation.Vertical)
            splitter_vertical.addWidget(right_frame)

            splitter = QSplitter(QtCore.Qt.Orientation.Horizontal)
            splitter.addWidget(left_frame)
            splitter.addWidget(right_frame)

            self_layout.addWidget(splitter)

            # Plot
            fig = Figure(figsize=(6, 6), dpi=100)
            axes = fig.add_subplot(111)
            canvas = FigureCanvasQTAgg(fig)
            self.set_plot(axes, added_log_instructions, deleted_log_instructions)
            toolbar = NavigationToolbar(canvas)
            right_layout.addWidget(toolbar)
            right_layout.addWidget(canvas)
            
            self.show()  # Show the widget
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))

    def _create_plot(self,width, height, dpi):
        try:
            fig = Figure(figsize=(width, height), dpi=dpi)
            axes = fig.add_subplot(111)
            canvas = FigureCanvasQTAgg(fig)
            return canvas, axes
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))
        
    

    def set_log_instruction(self, log_instructions_added, log_instructions_deleted):
        try:
            for log_instruction_add in log_instructions_added:
                # Add each commit information as an item to the QListWidget
                if(log_instruction_add.instruction is not None):
                    item = QListWidgetItem(log_instruction_add.instruction.replace("  ","") + "\tnumber of time modified : " + str(len(log_instruction_add.modifications)))
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

            for added_log in log_instructions_added:
                print(added_log.instruction)
                print(added_log.modifications[0].get_commit_hash())
                for modif in added_log.modifications:
                    print(modif.get_date())

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
            axes.set_xticklabels([date.strftime('%Y-%m-%d') for date in dates_added], rotation=90, ha='right')
        except Exception as e:
            traceback.print_exc()
            PopupManager.show_error_popup("Caught Error", str(e))
