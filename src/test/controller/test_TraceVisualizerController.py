import unittest
import json
from unittest.mock import Mock, patch, MagicMock
from model.GraphBuilders.GraphManager import GraphManager
from model.LogInstructionCollectors.Modification import Modification
from model.LogInstructionCollectors.LogInstruction import LogInstruction
from controller.TraceVisualizerController import TraceVisualizerController
from model.LogInstructionCollectors.Log4pCollector import Log4pCollector
from model.LogInstructionCollectors.Log4jCollector import Log4jCollector
from unittest.mock import MagicMock, patch
from PyQt6.QtWidgets import QLineEdit, QApplication, QMessageBox
from PyQt6.QtCore import Qt
from model.LogInstructionsFileGenerators.CsvFileGenerator import CsvFileGenerator
from model.LogInstructionsFileGenerators.JsonFileGenerator import JsonFileGenerator

from view.TraceVisualizerView import TraceVisualizerView

class test_TraceVisualizerController(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])
        
    def test_TraceVisualizerController_(self):
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
            tvc = TraceVisualizerController.fromArgs([QLineEdit('log4p')], 'from_date', 'to_date', 'repo_path', 'searched_path', 'searched_branch', 'searched_author')
        mock_get_log_instructions.assert_called_once()
        mock_set_graphic.assert_called_once()
        mock_build_graph.assert_called_once()
        self.assertIsInstance(tvc.log_instruction_collector, Log4pCollector)

    def test_TraceVisualizerController_Log4j(self):
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
        with patch('model.LogInstructionCollectors.Log4jCollector.Log4jCollector.get_log_instructions', mock_get_log_instructions), \
            patch('view.TraceVisualizerView.TraceVisualizerView.set_graphic', mock_set_graphic),\
            patch('model.GraphBuilders.GraphBuilder.GraphBuilder.build_graph', mock_build_graph) :
            tvc = TraceVisualizerController.fromArgs([QLineEdit('log4j')], 'from_date', 'to_date', 'repo_path', 'searched_path', 'searched_branch', 'searched_author')
        mock_get_log_instructions.assert_called_once()
        mock_set_graphic.assert_called_once()
        mock_build_graph.assert_called_once()
        self.assertIsInstance(tvc.log_instruction_collector, Log4jCollector)
        
    def test_set_strategy_collector(self):
        collector = TraceVisualizerController._set_strategy_collector('log4p')
        self.assertIsInstance(collector, Log4pCollector)
        collector = TraceVisualizerController._set_strategy_collector('log4j')
        self.assertIsInstance(collector, Log4jCollector)
        with self.assertRaises(ValueError):
            TraceVisualizerController._set_strategy_collector('invalid')

    def test_set_strategy_generator_file(self):
        controller = TraceVisualizerController([])
        generator = controller._set_strategy_generator_file('csv')
        self.assertIsInstance(generator, CsvFileGenerator)
        with self.assertRaises(ValueError):
            controller._set_strategy_generator_file('invalid')

    @patch('PyQt6.QtWidgets.QFileDialog.getSaveFileName', return_value=('filename.json', ''))
    @patch.object(JsonFileGenerator, 'createFile')
    @patch.object(QMessageBox, 'exec')
    def test_save_data(self, mock_exec, mock_create_file, mock_get_save_file_name):
        controller = TraceVisualizerController([])
        controller.all_log_instructions = [Mock()]
        controller._save_data()
        mock_get_save_file_name.assert_called_once()
        mock_create_file.assert_called_once()
        mock_exec.assert_called_once()
   

if __name__ == "__main__":
    unittest.main()