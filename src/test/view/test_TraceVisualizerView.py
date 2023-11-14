import unittest
from model.LogInstructionCollectors.LogInstruction import LogInstruction
from model.LogInstructionCollectors.Modification import Modification
from unittest.mock import Mock, MagicMock
from model.LogInstructionsFileGenerators.CsvFileGenerator import CsvFileGenerator
from model.GraphBuilders.GraphManager import GraphBuilder
from view.TraceVisualizerView import TraceVisualizerView
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QApplication, QFrame
import matplotlib.pyplot as plt




class test_TraceVisualizerView(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
      cls.app = QApplication([])
    
  def test_TraceVisualizerView_init(self):
     tvv = TraceVisualizerView()
     self.assertIsNone(tvv.graphic)
     self.assertIsNotNone(tvv.right_layout)

  def test_TraceVisualizerView_Plot(self):
     tvv = TraceVisualizerView()
     tvv.log_instructions_list.addItem = Mock()
     modification = Modification('commit', 'instruction','date', 'type', 'beforeCode', 'aftercode', 'hash', 'filename', 'author')
     modification2 = Modification('commit', 'instruction','date', 'deleted', 'beforeCode', 'aftercode', 'hash', 'filename', 'author')

     logInstruction = LogInstruction('info','"info"', [modification], '2023-01-01')
     logInstruction2 = LogInstruction('info','"info"', [modification2], '2023-01-01')
     tvv.set_log_instructions( log_instructions=[logInstruction])
     tvv.log_instructions_list.addItem.assert_called()

  
  def test_Graphic_None(self):
     tvv = TraceVisualizerView()
     try:
      tvv.set_graphic(None)
     except ValueError as e:
      self.assertEqual(str(e),"graphic cannot be None")


if __name__ == "__main__":
    unittest.main()