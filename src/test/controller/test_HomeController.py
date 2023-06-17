import unittest
from controller.HomeController import HomeController
from unittest.mock import Mock, patch, MagicMock
from model.LogInstruction import LogInstruction
from model.Modification import Modification
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication
from io import StringIO
from unittest.mock import patch
import os
import sys



class test_HomeController(unittest.TestCase):
        
    
    def test_validate_date_range_range_valid(self):
        homePage = Mock()
        homeModel =  Mock()
        homePage.repoList.currentText =  MagicMock(return_value='path')
        homeController = HomeController(homePage, homeModel)
        homePage.from_calendar.selectedDate = MagicMock(return_value=QDate(2023, 1, 1))
        homePage.to_calendar.selectedDate = MagicMock(return_value=QDate(2023, 1, 2))
        captured_output = StringIO()
        sys.stdout = captured_output
        homeController.validate_date_range()
        printed_output = captured_output.getvalue().strip()
        homePage.from_date_label.setText.assert_called_once_with("FROM: Sun Jan 1 2023")
        homePage.to_date_label.setText.assert_called_once_with("TO: Mon Jan 2 2023")
        self.assertEqual(printed_output, "Valid date range")

    def test_validate_date_range_range_invalid(self):
        homePage = Mock()
        homeModel =  Mock()
        homePage.repoList.currentText =  MagicMock(return_value='path')
        homeController = HomeController(homePage, homeModel)
        homePage.from_calendar.selectedDate = MagicMock(return_value=QDate(2023, 1, 2))
        homePage.to_calendar.selectedDate = MagicMock(return_value=QDate(2023, 1, 1))
        homeController.validate_date_range()
        homePage.from_date_label.setText.assert_called_once_with("FROM: Mon Jan 2 2023")
        homePage.to_date_label.setText.assert_called_once_with("TO: Sun Jan 1 2023")
        homePage.popupError.assert_called_once_with("Invalid Date Range", "La date 'FROM' ne peut pas être postérieure à la date 'TO'.")

    def test_new_repo_button_clicked(self):
        app = QApplication([])
        homePage = Mock()
        homeModel =  Mock()
        homePage.repoList.currentText =  MagicMock(return_value='path')
        homeController = HomeController(homePage, homeModel)
        homeController.new_repo_button_clicked()
        self.assertIsNotNone(homeController.NewRepoView)
        self.assertIsNotNone(homeController.NewRepoModel)
        self.assertIsNotNone(homeController.NewRepoController)


    def test_create_directory_existing_path(self):
        homePage = Mock()
        homeModel =  Mock()
        homePage.repoList.currentText =  MagicMock(return_value='path')
        homeController = HomeController(homePage, homeModel)
        mock_os = Mock()
        with patch('os.makedirs', mock_os):
            homeController.create_directory('./test/test/test_HomeController.py')
            mock_os.assert_called_once_with('./test/test/test_HomeController.py')
    @patch('os.makedirs')
    def create_directory_OsError(self, mock_os):
         homePage = Mock()
         homeModel =  Mock()
         mock_os = Mock(side_effect= OSError('test'))
         homePage.repoList.currentText =  MagicMock(return_value='path')
         homeController = HomeController(homePage, homeModel)
         captured_output = StringIO()
         sys.stdout = captured_output
         homeController.create_directory('./<user>/controller/test_HomeController.py')
         printed_output = captured_output.getvalue().strip()
         self.assertIn("An error occurred while creating the directory: ", printed_output)

    def test_search_button_clicked(self):
        app = QApplication([])
        homePage = Mock()
        homeModel =  Mock()
        modification = Modification('commit', 'date', 'type', 'beforeCode', 'aftercode', 'hash', 'filename')
        modification2 = Modification('commit', 'date', 'deleted', 'beforeCode', 'aftercode', 'hash', 'filename')
        logInstruction = LogInstruction('log.info("info")', [modification], '2023-01-01')
        logInstruction2 = LogInstruction('log.info("info")', [modification2], '2023-01-01')
        homeModel.get_log_instructions = MagicMock(return_value= ([logInstruction], [logInstruction2]))
        homePage.repoList.currentText =  MagicMock(return_value='path')
        homeController = HomeController(homePage, homeModel)
        homePage.from_calendar.selectedDate = MagicMock(return_value=QDate(2023, 1, 1))
        homePage.to_calendar.selectedDate = MagicMock(return_value=QDate(2023, 1, 2))
        captured_output = StringIO()
        sys.stdout = captured_output
        homeController.search_button_clicked()
        self.assertIsNotNone(homeController.traceVisualizerView)
        self.assertIsNotNone(homeController.traceVisualizerModel)
        self.assertIsNotNone(homeController.traceVisualizerController)

    def test_delete_repo_button_clicked(self):
        app = QApplication([])
        homePage = Mock()
        homeModel =  Mock()
        homePage.repoList.currentText =  MagicMock(return_value='path')
        homeController = HomeController(homePage, homeModel)
        homePage.from_calendar.selectedDate = MagicMock(return_value=QDate(2023, 1, 1))
        homePage.to_calendar.selectedDate = MagicMock(return_value=QDate(2023, 1, 2))
        homeController.delete_repo_button_clicked()
        homeModel.deleteRepo.assert_called_once()



    

        
   

if __name__ == "__main__":
    unittest.main()