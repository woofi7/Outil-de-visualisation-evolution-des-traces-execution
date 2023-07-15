import unittest
from controller.HomeController import HomeController
from unittest.mock import Mock, patch, MagicMock
from model.LogInstructionCollectors.LogInstruction import LogInstruction
from model.LogInstructionCollectors.Modification import Modification
from controller.TraceVisualizerController import TraceVisualizerController
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication
from io import StringIO
from unittest.mock import patch
import os
import sys



class test_HomeController(unittest.TestCase):
        
    
    def test_validate_date_range_range_valid(self):
        app = QApplication([])
        homePage = Mock()
        homeModel =  Mock()
        homePage.repoList.currentText =  MagicMock(return_value='path')
        homeController = HomeController()
        homeController.repos_manager.get_repos = MagicMock(return_value=['path'])
        homeController.home_view= Mock()
        homeController.home_view.from_calendar.selectedDate = MagicMock(return_value=QDate(2023, 1, 1))
        homeController.home_view.to_calendar.selectedDate = MagicMock(return_value=QDate(2023, 1, 2))
        captured_output = StringIO()
        sys.stdout = captured_output
        homeController._validate_date_range()
        printed_output = captured_output.getvalue().strip()
        homeController.home_view.from_date_label.setText.assert_called_once_with("FROM: Sun Jan 1 2023")
        homeController.home_view.to_date_label.setText.assert_called_once_with("TO: Mon Jan 2 2023")
        self.assertEqual(printed_output, "Valid date range")

    def test_validate_date_range_range_invalid(self):
        app = QApplication([])
        homePage = Mock()
        homeModel =  Mock()
        homeController = HomeController()
        homeController.repos_manager.get_repos = MagicMock(return_value=['path'])
        homeController.home_view= Mock()
        homePage.repoList.currentText =  MagicMock(return_value='path')
        homeController.home_view.from_calendar.selectedDate = MagicMock(return_value=QDate(2023, 1, 2))
        homeController.home_view.to_calendar.selectedDate = MagicMock(return_value=QDate(2023, 1, 1))
        homeController._validate_date_range()
        homeController.home_view.from_date_label.setText.assert_called_once_with("FROM: Mon Jan 2 2023")
        homeController.home_view.to_date_label.setText.assert_called_once_with("TO: Sun Jan 1 2023")
        homeController.home_view.popupError.assert_called_once_with("Invalid Date Range", "La date 'FROM' ne peut pas être postérieure à la date 'TO'.")

    def test_new_repo_button_clicked(self):
        app = QApplication([])
        homePage = Mock()
        homeModel =  Mock()
        homePage.repoList.currentText =  MagicMock(return_value='path')
        homeController = HomeController()
        homeController.repos_manager.get_repos = MagicMock(return_value=['path'])
        homeController._new_repo_button_clicked()
        self.assertIsNotNone(homeController.new_repo_controller)

    @patch('controller.TraceVisualizerController.TraceVisualizerController.__init__')
    def test_search_button_clicked(self, mock_trace_visualizer_controller):
        app = QApplication([])
        homePage = Mock()
        homeModel =  Mock()
        modification = Modification('commit','instruction', 'date', 'type', 'beforeCode', 'aftercode', 'hash', 'filename')
        modification2 = Modification('commit','instruction' ,'date', 'deleted', 'beforeCode', 'aftercode', 'hash', 'filename')
        logInstruction = LogInstruction('log.info("info")','instruction', [modification], '2023-01-01')
        logInstruction2 = LogInstruction('log.info("info")','instruction', [modification2], '2023-01-01')
        homeModel.get_log_instructions = MagicMock(return_value= ([logInstruction], [logInstruction2]))
        homePage.repoList.currentText =  MagicMock(return_value='path')
        homeController = HomeController()
        homeController.repos_manager.get_repos = MagicMock(return_value=['path'])
        homeController.repos_manager.git_pull = Mock()
        homeController.home_view.from_calendar.selectedDate = MagicMock(return_value=QDate(2023, 1, 1))
        homeController.home_view.to_calendar.selectedDate = MagicMock(return_value=QDate(2023, 1, 2))
        captured_output = StringIO()
        sys.stdout = captured_output
        mock_trace_visualizer_controller.return_value = None
        homeController._search_button_clicked()
        mock_trace_visualizer_controller.assert_called_once()

    def test_delete_repo_button_clicked(self):
        app = QApplication([])
        homePage = Mock()
        homeController = HomeController()
        homeController.repos_manager.get_repos = MagicMock(return_value=['path'])
        homeController.home_view.setRepos = MagicMock(return_value=['path'])
        homeController.repos_manager.deleteRepo =  Mock()
        homePage.repoList.currentText =  MagicMock(return_value='path')
        homePage.from_calendar.selectedDate = MagicMock(return_value=QDate(2023, 1, 1))
        homePage.to_calendar.selectedDate = MagicMock(return_value=QDate(2023, 1, 2))
        homeController._delete_repo_button_clicked()
        homeController.repos_manager.deleteRepo.assert_called_once()



    

        
   

if __name__ == "__main__":
    unittest.main()