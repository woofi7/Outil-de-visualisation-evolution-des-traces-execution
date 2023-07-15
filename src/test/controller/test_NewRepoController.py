import unittest
from unittest.mock import Mock
from controller.NewRepoController import NewRepoController
from unittest.mock import MagicMock
from PyQt6.QtWidgets import QLineEdit, QApplication



class test_NewRepoController(unittest.TestCase):
        
    
    def test_ok_button_clicked(self):
        app = QApplication([])
        view = Mock()
        model = Mock()
        homeController = Mock()
        view.newRepo = MagicMock(return_values = QLineEdit('test/test/test.py'))
        newRepoController = NewRepoController(view, model, homeController)
        newRepoController._ok_button_clicked()
        model.cloneRepo.assert_called_once()
        view.close.assert_called_once()
        homeController.update_repo_list.assert_called_once()

    def test_cancel_button_clicked(self):
        app = QApplication([])
        view = Mock()
        model = Mock()
        homeController = Mock()
        view.newRepo = MagicMock(return_values = QLineEdit('test/test/test.py'))
        newRepoController = NewRepoController(view, model, homeController)
        newRepoController._cancel_button_clicked()
        view.close.assert_called_once()

        


   

if __name__ == "__main__":
    unittest.main()