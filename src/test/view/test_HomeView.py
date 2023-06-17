import unittest
from model.NewRepoModel import NewRepoModel
from unittest.mock import Mock, MagicMock, patch
from view.HomeView import HomeView
from PyQt6.QtWidgets import QApplication
from view.PopupView import PopupManager
import traceback




class test_HomeView(unittest.TestCase):
        

    
  def test_HomeView_init(self):
     app = QApplication([])
     view = HomeView()
     self.assertIsNotNone(view.repoList)
     self.assertIsNotNone(view.newRepoButton)
     self.assertIsNotNone(view.deleteRepoButton)
     self.assertIsNotNone(view.searched_path)
     self.assertIsNotNone(view.branches)
     self.assertIsNotNone(view.searched_author)
     self.assertIsNotNone(view.slected_framework)
     self.assertIsNotNone(view.from_date_label)
     self.assertIsNotNone(view.from_calendar)
     self.assertIsNotNone(view.to_date_label)
     self.assertIsNotNone(view.to_calendar)

  def test_HomeView_setRepos(self):
     app = QApplication([])
     view = HomeView()
     view.setRepos(['repo1', 'repo2'] )
     self.assertEqual(len(view.repos), 2) 

  def HomeView_setRepos_Exception(self):
     app = QApplication([])
     PopupManager.show_error_popup = Mock()
     traceback.print_exc = Mock()
     view = HomeView()
     view.repoList.addItem = Mock(side_effect = Exception("Mocked exception"))
     view.setRepos(['repo1', 'repo2'] )
     PopupManager.show_error_popup.assert_called_once()
     traceback.print_exc.assert_called_once()

  def test_HomeView_setBranche(self):
     app = QApplication([])
     view = HomeView()
     view.setBranches(['branche1', 'branche'] )
     self.assertEqual(len(view.branches), 2) 

  @patch('view.PopupView.PopupManager.show_error_popup')
  @patch('traceback.print_exc')
  def HomeView_setBranch_Exception(self, mock_popup, mock_traceback):
     app = QApplication([])
     mock_popup = Mock()
     mock_traceback = Mock()
     view = HomeView()
     view.branches.addItem = Mock(side_effect = Exception("Mocked exception"))
     view.setBranches(['branche1', 'branche'] )
     mock_popup.assert_called_once()
     #traceback.print_exc.assert_called_once()


if __name__ == "__main__":
    unittest.main()