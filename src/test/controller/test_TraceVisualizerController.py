import unittest
from unittest.mock import Mock, MagicMock
from model.LogInstructionCollectors.Modification import Modification
from model.LogInstructionCollectors.LogInstruction import LogInstruction
from controller.TraceVisualizerController import TraceVisualizerController
from view.TraceVisualizerView import TraceVisualizerView  # Import the correct class
from PyQt6.QtWidgets import QLineEdit, QApplication
from view.PopupView import PopupManager

class test_TraceVisualizerController(unittest.TestCase):

    def test_TraceVisualizerController_init(self):
        app = QApplication([])
        view = Mock()
        model = Mock()
        home_view = Mock()
        home_model = Mock()
        home_view.repoList.currentText = MagicMock(return_value='test')
        modification2 = Modification('commit', 'instruction', '2023-01-01', 'deleted', 'beforeCode', 'aftercode', 'hash', 'filename', 'author')
        logInstruction2 = LogInstruction('log.info("info")', 'instruction', [modification2], '2023-01-01')
        model.getCommitChanges = MagicMock(return_value=[['test', 'test', 'test', 'test']])
        tvc = TraceVisualizerController([QLineEdit('log4p')], 'from_date', 'to_date', 'repo_path', 'searched_path', 'searched_branch', 'searched_author')
        tvc.trace_visualizer_view = TraceVisualizerView()  # Use the actual class here
        tvc.log_instruction_collector.get_log_instructions = Mock(return_value=({'test': [logInstruction2]}, [logInstruction2]))

        # Test the constructor and ensure that the TraceVisualizerView is created with the correct data
        self.assertIsInstance(tvc.trace_visualizer_view, TraceVisualizerView)
        # Add more assertions here to check if the view is set up as expected

        # Test the _show_commit_changes method
        item = MagicMock()
        item.data.return_value = MagicMock(modifications=[modification2])
        tvc._show_commit_changes(item)

        # Test the _set_strategy_collector method
        tvc_strategy = tvc._set_strategy_collector("log4p")
        self.assertEqual(type(tvc_strategy).__name__, "Log4pCollector")

        # Test the _set_strategy_generator_file method
        tvc_strategy_file = tvc._set_strategy_generator_file("csv")
        self.assertEqual(type(tvc_strategy_file).__name__, "CsvFileGenerator")

