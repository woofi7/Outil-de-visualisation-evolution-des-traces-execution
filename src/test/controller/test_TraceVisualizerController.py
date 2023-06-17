import unittest
from unittest.mock import Mock
from model.Modification import Modification
from model.LogInstruction import LogInstruction
from controller.TraceVisualizerController import TraceVisualizerController
from unittest.mock import MagicMock
from PyQt6.QtWidgets import QLineEdit, QApplication
from view.PopupView import PopupManager
import traceback



class test_TraceVisualizerController(unittest.TestCase):
        
    
    def test_TraceVisualizerController_init(self):
        app = QApplication([])
        view = Mock()
        model = Mock()
        home_view = Mock()
        home_model = Mock()
        home_view.repoList.currentText = MagicMock(return_value='test')
        modification2 = Modification('commit', 'date', 'deleted', 'beforeCode', 'aftercode', 'hash', 'filename')
        logInstruction2 = LogInstruction('log.info("info")', [modification2], '2023-01-01')
        model.getCommitChanges = MagicMock(return_value = [['test', 'test', 'test', 'test']] )
        tvc = TraceVisualizerController(view, model, home_view, home_model)
   

if __name__ == "__main__":
    unittest.main()