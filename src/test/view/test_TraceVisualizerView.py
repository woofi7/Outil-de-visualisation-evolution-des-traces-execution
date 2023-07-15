import unittest
from model.LogInstructionCollectors.LogInstruction import LogInstruction
from model.LogInstructionCollectors.Modification import Modification
from unittest.mock import Mock, MagicMock
from view.TraceVisualizerView import TraceVisualizerView
from PyQt6.QtWidgets import QApplication



class test_TraceVisualizerView(unittest.TestCase):

    
  def test_TraceVisualizerView_init(self):
     app = QApplication([])
     tvv = TraceVisualizerView()
     self.assertIsNone(tvv.graphic)
     self.assertIsNotNone(tvv.right_layout)

  def test_TraceVisualizerView_Plot(self):
     app = QApplication([])
     tvv = TraceVisualizerView()
     tvv.log_instructions_list.addItem = Mock()
     modification = Modification('commit', 'instruction','date', 'type', 'beforeCode', 'aftercode', 'hash', 'filename')
     modification2 = Modification('commit', 'instruction','date', 'deleted', 'beforeCode', 'aftercode', 'hash', 'filename')

     logInstruction = LogInstruction('info','"info"', [modification], '2023-01-01')
     logInstruction2 = LogInstruction('info','"info"', [modification2], '2023-01-01')
     tvv.set_log_instructions( log_instructions={'list':[logInstruction]}, deleted_instruction=[logInstruction2])
     tvv.log_instructions_list.addItem.assert_called()
   
  def test_TraceVisualizerView_None_instruction(self):
     app = QApplication([])
     tvv = TraceVisualizerView()
     tvv.log_instructions_list.addItem = Mock()
     modification = Modification('commit', 'instruction','date', 'type', 'beforeCode', 'aftercode', 'hash', 'filename')
     modification2 = Modification('commit', 'instruction','date', 'deleted', 'beforeCode', 'aftercode', 'hash', 'filename')

     logInstruction = LogInstruction('info','"info"', [modification], '2023-01-01')
     logInstruction2 = LogInstruction('info','"info"', [modification2], '2023-01-01')
     try:
         tvv.set_log_instructions( log_instructions=None, deleted_instruction=None)
     except ValueError as e:
         self.assertEqual(str(e),'log_instructions cannot be None')
     tvv.log_instructions_list.addItem.assert_not_called()
  
  def test_Graphic_None(self):
     app = QApplication([])
     tvv = TraceVisualizerView()
     try:
      tvv.set_graphic(None)
     except ValueError as e:
      self.assertEqual(str(e),"graphic cannot be None")

  def test_Graphic(self):
     app = QApplication([])
     tvv = TraceVisualizerView()
     graphic = MagicMock(return_value='graphic')
     tvv.right_layout.removeWidget = Mock()
     graphic.setGeometry = Mock()
     tvv.right_layout.addWidget = Mock()
     tvv.set_graphic(graphic)
     tvv.right_layout.addWidget.assert_called()
     graphic.setGeometry.assert_called()



if __name__ == "__main__":
    unittest.main()