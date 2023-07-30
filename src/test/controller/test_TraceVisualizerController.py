import unittest
from unittest.mock import Mock
from model.LogInstructionCollectors.Modification import Modification
from model.LogInstructionCollectors.LogInstruction import LogInstruction
from controller.TraceVisualizerController import TraceVisualizerController
from model.LogInstructionCollectors.Log4pCollector import Log4pCollector
from unittest.mock import MagicMock, patch
from PyQt6.QtWidgets import QLineEdit, QApplication
from view.PopupView import PopupManager
import traceback



class test_TraceVisualizerController(unittest.TestCase):
        
    def test_TraceVisualizerController_(self):
        app = QApplication([])
        view = Mock()
        model = Mock()
        home_view = Mock()
        home_model = Mock()
        home_view.repoList.currentText = MagicMock(return_value='test')
        modification2 = Modification('commit','instruction', '2023-01-01', 'deleted', 'beforeCode', 'aftercode', 'hash', 'filename', 'author')
        logInstruction2 = LogInstruction('log.info("info")', 'instruction',[modification2], '2023-01-01')
        model.getCommitChanges = MagicMock(return_value = [['test', 'test', 'test', 'test']] )
        mock_get_log_instructions = MagicMock(return_value = ([logInstruction2]))
        mock_set_graphic = MagicMock()
        mock_build_graph = MagicMock()
        with patch('model.LogInstructionCollectors.Log4pCollector.Log4pCollector.get_log_instructions', mock_get_log_instructions), \
            patch('view.TraceVisualizerView.TraceVisualizerView.set_graphic', mock_set_graphic),\
            patch('model.GraphBuilders.GraphBuilder.GraphBuilder.build_graph', mock_build_graph) :
            tvc = TraceVisualizerController([QLineEdit('log4p')], 'from_date', 'to_date', 'repo_path', 'searched_path', 'searched_branch', 'searched_author')
        mock_get_log_instructions.assert_called_once()
        mock_set_graphic.assert_called_once()
        mock_build_graph.assert_called_once()
        self.assertIsInstance(tvc.log_instruction_collector, Log4pCollector)

   

if __name__ == "__main__":
    unittest.main()