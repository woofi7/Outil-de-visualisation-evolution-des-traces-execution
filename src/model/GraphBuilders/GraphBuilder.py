from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import MaxNLocator
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class GraphBuilder:

     def build_graph(self, path_to_file_csv):
        # Read the csv file
        logData = pd.read_csv(path_to_file_csv)
     
        # Sort the dates in ascending order
        logData['Date'] = pd.to_datetime(logData['Date'])
        logData = logData.sort_values(by='Date')
     
        # Create a new column to store the Log index value for each index
        logData['Log index'] = logData.groupby('Index').cumcount()
     
        # Replace the y values with the actual index values
        logData['Log index'] = logData['Index']
     
        fig, ax = plt.subplots()
        plt.style.use("ggplot")
        plt.xticks(rotation=30)
        sns.lineplot(data=logData, x="Date", y="Log index", hue="Index", marker="o")
        # Retirer la légende
        ax.legend().remove()
     
        canvas = FigureCanvas(fig)
        scene = QGraphicsScene()
        scene.addWidget(canvas)
     
        view = QGraphicsView(scene)
     
        return view