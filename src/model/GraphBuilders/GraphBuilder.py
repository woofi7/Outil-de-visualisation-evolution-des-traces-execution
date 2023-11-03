from matplotlib.backend_bases import MouseEvent
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.collections import PathCollection
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter
from matplotlib.text import Annotation


def scroll_event(event: MouseEvent):
    xmin, xmax = plt.xlim()
    range = xmax - xmin
    if event.button == 'up':
        x = xmin + range / 20
    else:
        x = xmin - range / 20

    plt.xlim(x, x + range)

    plt.draw()
    pass


class GraphBuilder:

    def build_graph(self, path_to_file_csv, instruction=-1, from_date=0, to_date=0):
        # Map the type values to colors
        color_map = {'ModificationType.ADD': 'green', 'ModificationType.MODIFY': 'blue',
                     'ModificationType.DELETE': 'red'}

        # Read the csv file
        log_data = pd.read_csv(path_to_file_csv)

        # Sort the dates in ascending order
        log_data['date'] = pd.to_datetime(log_data['date'], utc=True)
        log_data = log_data.sort_values(by=['index', 'date'])

        fig, ax = plt.subplots()
        plt.style.use("ggplot")
        plt.xticks(rotation=30)
        plt.xlim(pd.to_datetime(from_date), pd.to_datetime(to_date))

        y_labels = {}

        plt.style.use("ggplot")
        plt.xticks(rotation=30)
        y_labels = {}

        offset_index = 0
        annotations = []
        for index, group in log_data.groupby('index'):
            x_values = group['date']
            y_values = [index] * len(x_values)
            group_instruction = group['instruction'].iloc[0][:16] + "..." if len(group['instruction'].iloc[0]) > 16 else \
                group['instruction'].iloc[0]
            y_labels[index] = group_instruction
            type_values = group['type']

            # Determine the size of the marker based on the instruction
            if index == instruction:
                marker_size = 60
            else:
                marker_size = 14

            for idx, x in enumerate(x_values):
                y = float(index)
                scatter = ax.scatter(x, y, marker='o', c=[color_map.get(type_values[offset_index], 'gray')],
                                     s=marker_size)
                annotation = ax.annotate(group['instruction'].iloc[idx],
                                         xy=(x, y),
                                         textcoords="offset points",
                                         bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                                         xytext=(10, 10),
                                         ha='center',
                                         visible=False)
                annotations.append((annotation, scatter))
                offset_index += 1
            plot = ax.plot(x_values, y_values, linestyle='-', color='gray')

        # Configure axis labels and legend
        date_format = DateFormatter("%Y/%m/%d")
        ax.xaxis.set_major_formatter(date_format)
        ax.set_xlabel('Date (YYYY/MM/DD)')
        ax.set_ylabel('Instruction')
        ax.set_yticks(list(y_labels.keys()))  # Set y-ticks based on the index
        ax.set_yticklabels(list(y_labels.values()))

        # Add legend
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='Added', markerfacecolor='green', markersize=8),
            Line2D([0], [0], marker='o', color='w', label='Modified', markerfacecolor='blue', markersize=8),
            Line2D([0], [0], marker='o', color='w', label='Deleted', markerfacecolor='red', markersize=8)]
        ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0.)

        canvas = FigureCanvas(fig)
        canvas.mpl_connect('scroll_event', lambda event: self.scroll_event(event))
        canvas.mpl_connect("motion_notify_event", lambda event: self.hover(event, annotations, canvas))
        canvas.mpl_connect('scroll_event', lambda event: scroll_event(event))
        return canvas


    def hover(self, event: MouseEvent, annotations: list[(Annotation, PathCollection)], canvas):
        for annotation, scatter in annotations:
            contains = scatter.contains(mouseevent=event)[0]
            if contains:
                if not (annotation.get_visible()):
                    annotation.set_visible(True)
                    plt.draw()
            else:
                if annotation.get_visible():
                    annotation.set_visible(False)
                    plt.draw()

   def scroll_event(self, event: MouseEvent):
      xmin, xmax = plt.xlim()

      print(event.x)
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
