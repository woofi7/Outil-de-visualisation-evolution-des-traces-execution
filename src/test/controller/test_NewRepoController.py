import unittest
from unittest.mock import Mock
from controller.NewRepoController import NewRepoController
from unittest.mock import MagicMock
from PyQt6.QtWidgets import QLineEdit, QApplication



class test_NewRepoController(unittest.TestCase):
        
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])
    
    def test_ok_button_clicked(self):
        view = Mock()
        view.newRepo = MagicMock(return_values = QLineEdit('test/test/test.py'))
        newRepoController = NewRepoController(view)
        newRepoController.repo_manager.get_repos = Mock()
        newRepoController.repo_manager.clone_repo = Mock()
        newRepoController._clone_repo()
        newRepoController.repo_manager.clone_repo.assert_called_once()
        view.setRepos.assert_called_once()

    def test_cancel_button_clicked(self):
        view = Mock()
        view.newRepo = MagicMock(return_values = QLineEdit('test/test/test.py'))
        newRepoController = NewRepoController(view)
        newRepoController.new_repo_view = Mock()
        newRepoController._cancel_button_clicked()
        newRepoController.new_repo_view.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()