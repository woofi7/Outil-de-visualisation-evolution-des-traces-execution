import unittest
from model.GraphBuilders.GraphManager import GraphManager
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QApplication
from unittest.mock import MagicMock, Mock
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import MaxNLocator
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class test_GraphBuilder(unittest.TestCase):
        
    @classmethod
    def setUpClass(cls):
        cls.gen = GraphManager()
        cls.app = QApplication([])

    def test_build_graph(self):
        self.gen = GraphManager()
        figMock = Mock()
        axesMock = Mock()
        axesMock.legend().remove = Mock()
        QGraphicsScene.addWidget = Mock()
        FigureCanvas.__init__ = MagicMock(return_value = None)
        plt.subplots = MagicMock(return_value = (figMock, axesMock))
        plt.xticks = Mock()
        sns.lineplot = Mock()
        view =self.gen.init_graph('./files/graphData.csv')
        self.assertIsNotNone(view)
        plt.subplots.assert_called_once()


    