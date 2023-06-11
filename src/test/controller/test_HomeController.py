import unittest
from controller.HomeController import HomeController
from unittest.mock import Mock, patch
from unittest.mock import MagicMock
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication
from io import StringIO
from unittest.mock import patch
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

    # def test_create_directory_OsError(self):
    #     homePage = Mock()
    #     homeModel =  Mock()
    #     homePage.repoList.currentText =  MagicMock(return_value='path')
    #     homeController = HomeController(homePage, homeModel)
    #     captured_output = StringIO()
    #     sys.stdout = captured_output
    #     homeController.create_directory('./<user>/controller/test_HomeController.py')
    #     printed_output = captured_output.getvalue().strip()
    #     self.assertIn("An error occurred while creating the directory: ", printed_output)


@patch('test.controller.test_HomeController.MagicMock')
def test_create_directory_OsError(self, mock_magicmock):
    homePage = Mock()
    homeModel = Mock()
    mock_magicmock.return_value = 'path'
    homeController = HomeController(homePage, homeModel)

    # Capture the output
    captured_output = StringIO()
    sys.stdout = captured_output

    # Call the method under test
    homeController.create_directory('./<user>/controller/test_HomeController.py')

    # Reset sys.stdout to its original value
    sys.stdout = sys.__stdout__

    # Get the printed output
    printed_output = captured_output.getvalue().strip()

    # Assert the error message is present
    self.assertIn("An error occurred while creating the directory: ", printed_output)



        
   

if __name__ == "__main__":
    unittest.main()