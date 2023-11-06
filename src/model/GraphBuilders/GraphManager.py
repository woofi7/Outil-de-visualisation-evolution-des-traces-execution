from matplotlib.backend_bases import MouseEvent
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.collections import PathCollection
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter
from matplotlib.text import Annotation


class GraphManager:
    color_map = {'ModificationType.ADD': 'green', 'ModificationType.MODIFY': 'blue',
                 'ModificationType.DELETE': 'red'}
    _instance = None
    _data = None
    _fig = None
    _ax = None
    _highlighted_instruction = None
    _canvas = None
    _annotations: list[(Annotation, PathCollection)] = []

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(GraphManager, cls).__new__(cls)
        return cls._instance

    def init_graph(self, path_to_file_csv, from_date=0, to_date=0):

        self._fig, self._ax = plt.subplots()
        plt.style.use("ggplot")
        plt.xticks(rotation=30)
        plt.xlim(pd.to_datetime(from_date), pd.to_datetime(to_date))

        self.set_data(path_to_file_csv)

        plt.style.use("ggplot")
        plt.xticks(rotation=30)

        # Con_figure axis labels and legend
        date_format = DateFormatter("%Y/%m/%d")
        self._ax.xaxis.set_major_formatter(date_format)
        self._ax.set_xlabel('Date (YYYY/MM/DD)')
        self._ax.set_ylabel('Instruction')

        # Add legend
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='Added', markerfacecolor='green', markersize=8),
            Line2D([0], [0], marker='o', color='w', label='Modified', markerfacecolor='blue', markersize=8),
            Line2D([0], [0], marker='o', color='w', label='Deleted', markerfacecolor='red', markersize=8)]
        self._ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0.)

        self._canvas = FigureCanvas(self._fig)
        self._canvas.mpl_connect('scroll_event', lambda event: self.scroll_event(event))
        self._canvas.mpl_connect("motion_notify_event", lambda event: self.hover(event))
        return self._canvas

    def set_highlighted_instruction(self, element_id):
        self._highlighted_instruction = element_id
        self.update_graph()

    def set_data(self, path_to_file_csv):
        self._data = pd.read_csv(path_to_file_csv)
        self._data['date'] = pd.to_datetime(self._data['date'], utc=True)
        self._data = self._data.sort_values(by=['index', 'date'])

        self.update_graph()

    def update_graph(self):
        for line in plt.gca().lines:
            line.remove()

        for scatter in plt.gca().collections:
            scatter.remove()

        y_labels = {}
        offset_index = 0
        for index, group in self._data.groupby('index'):
            x_values = group['date']
            y_values = [index] * len(x_values)
            group_instruction = group['instruction'].iloc[0][:16] + "..." if len(group['instruction'].iloc[0]) > 16 else \
                group['instruction'].iloc[0]
            y_labels[index] = group_instruction
            type_values = group['type']

            # Determine the size of the marker based on the instruction
            if index == self._highlighted_instruction:
                marker_size = 60
            else:
                marker_size = 14

            for idx, x in enumerate(x_values):
                y = float(index)
                scatter = self._ax.scatter(x, y, marker='o', c=[self.color_map.get(type_values[offset_index], 'gray')],
                                           s=marker_size)
                annotation = ax.annotate("Author: " + group['author'].iloc[idx] + "\nChange Type: " + group['type'].iloc[idx].split(".")[1] + "\nInstruction: " + group['instruction'].iloc[idx],
                                         xy=(x, y),
                                         textcoords="offset points",
                                         bbox=dict(boxstyle='round,pad=0.5', fc='grey', alpha=0.8),
                                         xytext=(10, 10),
                                         ha='center',
                                         visible=False)
                self._annotations.append((annotation, scatter))
                offset_index += 1
            plot = self._ax.plot(x_values, y_values, linestyle='-', color='gray')
        self._ax.set_yticks(list(y_labels.keys()))
        self._ax.set_yticklabels(list(y_labels.values()))
        plt.draw()

    def scroll_event(self, event: MouseEvent):
        xmin, xmax = plt.xlim()

        if 'ctrl' in event.modifiers:
            if event.button == 'down':
                center = (xmax - xmin) / 2 + xmin
                range = (xmax - xmin) * 1.1
                xmin = center - range / 2
                xmax = center + range / 2
            else:
                current_range = xmax - xmin
                x_relative = (event.xdata - xmin)
                x_factor = x_relative / current_range

                range = (xmax - xmin) * 0.9
                range_offset = range - current_range

                left_offset = range_offset * x_factor
                right_offset = range_offset - left_offset

                xmin -= left_offset
                xmax += right_offset

            plt.xlim(xmin, xmax)

        else:
            xmin, xmax = plt.xlim()
            range = xmax - xmin
            if event.button == 'up':
                x = xmin + range / 20
            else:
                x = xmin - range / 20

            plt.xlim(x, x + range)

        plt.draw()

    def hover(self, event: MouseEvent):
        for annotation, scatter in self._annotations:
            contains = scatter.contains(mouseevent=event)[0]
            if contains:
                if not (annotation.get_visible()):
                    annotation.set_visible(True)
                    plt.draw()
            else:
                if annotation.get_visible():
                    annotation.set_visible(False)
                    plt.draw()