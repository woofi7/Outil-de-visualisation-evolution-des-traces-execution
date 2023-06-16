import unittest
from model.NewRepoModel import NewRepoModel
from model.LogInstruction import LogInstruction
from unittest.mock import Mock
from view.TraceVisualizerView import TraceVisualizerView
from PyQt6.QtWidgets import QApplication



class test_TraceVisualizerView(unittest.TestCase):

    
  def test_TraceVisualizerView_init(self):
     app = QApplication([])
     log_instruction = LogInstruction('test', [], '2023-01-01')
     tvv = TraceVisualizerView([],[])
     tvv.added_commits_list.addItem = Mock()
     tvv.deleted_commits_list.addItem = Mock()
     tvv.set_log_instruction([log_instruction, log_instruction], [log_instruction, log_instruction])
     tvv.added_commits_list.addItem.assert_called()
     tvv.deleted_commits_list.addItem.assert_called()
     self.assertIsNotNone(tvv.deleted_commits_list)
     


if __name__ == "__main__":
    unittest.main()