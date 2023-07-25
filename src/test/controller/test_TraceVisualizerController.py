import unittest
from unittest.mock import Mock
from model.LogInstructionCollectors.Modification import Modification
from model.LogInstructionCollectors.LogInstruction import LogInstruction
from controller.TraceVisualizerController import TraceVisualizerController
from unittest.mock import MagicMock
from PyQt6.QtWidgets import QLineEdit, QApplication
from view.PopupView import PopupManager
import traceback



class test_TraceVisualizerController(unittest.TestCase):
        
    
    def TraceVisualizerController_init(self):
        app = QApplication([])
        view = Mock()
        model = Mock()
        home_view = Mock()
        home_model = Mock()
        home_view.repoList.currentText = MagicMock(return_value='test')
        modification2 = Modification('commit','instruction', '2023-01-01', 'deleted', 'beforeCode', 'aftercode', 'hash', 'filename')
        logInstruction2 = LogInstruction('log.info("info")', 'instruction',[modification2], '2023-01-01')
        model.getCommitChanges = MagicMock(return_value = [['test', 'test', 'test', 'test']] )
        tvc = TraceVisualizerController([QLineEdit('log4p')], 'from_date', 'to_date', 'repo_path', 'searched_path', 'searched_branch', 'searched_author')
        tvc.trace_visualizer_view = Mock()
        tvc.log_instruction_collector.get_log_instructions = Mock(return_value = ({'test':[logInstruction2]}, [logInstruction2]))
   

if __name__ == "__main__":
    unittest.main()