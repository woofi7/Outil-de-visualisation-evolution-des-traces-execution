from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter


class GraphBuilder:

   def build_graph(self, path_to_file_csv, instruction=-1):
      # Map the type values to colors
      color_map = {'ModificationType.ADD': 'green', 'ModificationType.MODIFY': 'blue', 'ModificationType.DELETE': 'red'}

      # Read the csv file
      logData = pd.read_csv(path_to_file_csv)

      # Sort the dates in ascending order
      logData['date'] = pd.to_datetime(logData['date'])
      logData = logData.sort_values(by=['index', 'date'])

      fig, ax = plt.subplots()
      plt.style.use("ggplot")
      plt.xticks(rotation=30)
      
      y_labels = {}

      for index, group in logData.groupby('index'):
         x_values = group['date']
         y_values = [index] * len(x_values)
         group_instruction = group['instruction'].iloc[0][:16] + "..." if len(group['instruction'].iloc[0]) > 16 else group['instruction'].iloc[0]
         y_labels[index] = group_instruction
         type_values = group['type']
         
         # Determine the size of the marker based on the instruction
         if index == instruction:
            marker_size = 60
         else:
            marker_size = 14  
         ax.scatter(x_values, y_values, marker='o', c=[color_map.get(t, 'gray') for t in type_values], s=marker_size)
         ax.plot(x_values, y_values, linestyle='-', color='gray')

      # Configure axis labels and legend
      date_format = DateFormatter("%Y/%m/%d")
      ax.xaxis.set_major_formatter(date_format)
      ax.set_xlabel('Date (YYYY/MM/DD)')
      ax.set_ylabel('Instruction')
      ax.set_yticks(list(y_labels.keys()))  # Set y-ticks based on the index
      ax.set_yticklabels(list(y_labels.values()))

      # Add legend
      legend_elements = [Line2D([0], [0], marker='o', color='w', label='Added', markerfacecolor='green', markersize=7),
                         Line2D([0], [0], marker='o', color='w', label='Modified', markerfacecolor='blue', markersize=7),
                         Line2D([0], [0], marker='o', color='w', label='Deleted', markerfacecolor='red', markersize=7)]
      ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0.)

      canvas = FigureCanvas(fig)
      return canvas