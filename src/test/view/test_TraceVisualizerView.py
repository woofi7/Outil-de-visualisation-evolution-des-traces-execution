import unittest
from model.NewRepoModel import NewRepoModel
from model.LogInstructionCollectors.LogInstruction import LogInstruction
from model.LogInstructionCollectors.Modification import Modification
from unittest.mock import Mock
from view.TraceVisualizerView import TraceVisualizerView
from PyQt6.QtWidgets import QApplication



class test_TraceVisualizerView(unittest.TestCase):

    
  def test_TraceVisualizerView_init(self):
     app = QApplication([])
     log_instruction = LogInstruction('test', [], '2023-01-01')
     tvv = TraceVisualizerView([],[])
     tvv.log_instructions_list.addItem = Mock()
     tvv.deleted_commits_list.addItem = Mock()
     tvv.set_log_instructions([log_instruction, log_instruction], [log_instruction, log_instruction])
     tvv.log_instructions_list.addItem.assert_called()
     tvv.deleted_commits_list.addItem.assert_called()
     self.assertIsNotNone(tvv.deleted_commits_list)

  def test_TraceVisualizerView_Plot(self):
     app = QApplication([])
     log_instruction = LogInstruction('test', [], '2023-01-01')
     tvv = TraceVisualizerView([],[])
     axes = Mock()
     modification = Modification('commit', 'date', 'type', 'beforeCode', 'aftercode', 'hash', 'filename')
     modification2 = Modification('commit', 'date', 'deleted', 'beforeCode', 'aftercode', 'hash', 'filename')

     logInstruction = LogInstruction('log.info("info")', [modification], '2023-01-01')
     logInstruction2 = LogInstruction('log.info("info")', [modification2], '2023-01-01')
     tvv.set_plot(axes= axes, log_instructions_added=[logInstruction], log_instructions_deleted=[logInstruction2])
     axes.assert_called
     


if __name__ == "__main__":
    unittest.main()