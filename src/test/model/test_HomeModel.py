import unittest
from model.HomeModel import HomeModel
from unittest.mock import Mock, patch, MagicMock
from model.GlobalModel import GlobalModel
from model.DataModel import DataModel
from model.Instructions import Instructions
from pydriller import Repository
from model.LogInstruction import LogInstruction
from model.Modification import Modification
import os
from PyQt6.QtWidgets import QApplication




class test_HomeModel(unittest.TestCase):
        
    
  def test_get_log_instructions(self):
     model = HomeModel()
     Repository.traverse_commits = MagicMock(return_value=[])
     instruction =  Instructions("./test/test/test_HomeController.py", ['2023-01-01', '2023-02-01'], ['log4j'], [])
     modification = Modification('commit', 'date', 'type', 'beforeCode', 'aftercode', 'hash', 'filename')
     modification2 = Modification('commit', 'date', 'deleted', 'beforeCode', 'aftercode', 'hash', 'filename')
     data = DataModel('test', 'test', instruction)
     logInstruction = LogInstruction('log.info("info")', [modification], '2023-01-01')
     logInstruction2 = LogInstruction('log.info("info")', [modification2], '2023-01-01')
     data.logs = {'test':[logInstruction, logInstruction2]}
     GlobalModel.getRepoBranch = MagicMock(return_value = data)
     added_log, deleted_log = model.get_log_instructions('test', '2023-01-01', '2023-02-01', '', 'master', None, ['log4j'])
     self.assertEqual(len(added_log),1)
     self.assertEqual(len(deleted_log),1)
     self.assertEqual(added_log[0], logInstruction)
     self.assertEqual(deleted_log[0], logInstruction2)
     self.assertEqual(added_log, model.get_added_log_instructions())
     self.assertEqual(deleted_log, model.get_deleted_log_instructions())


  def test_getRepos(self):
     model = HomeModel()
     folder_name= model.get_repos('./')
     self.assertEqual(len(folder_name),8)

  @patch('view.PopupView.PopupManager.show_error_popup')
  @patch('traceback.print_exc')   
  def test_getRepos_exception(self, mock_popup, mock_traceback):
     mock_popup = Mock()
     mock_traceback = Mock()
     os.scandir = Mock(side_effect=Exception('test'))
     model = HomeModel()
     folder_name= model.get_repos('./')
     mock_popup.assert_called_once

  def test_on_rm_error(self):
      os.chmod = Mock()
      os.unlink = Mock()
      model = HomeModel()
      model.on_rm_error('test', 'test', 'test')
      os.chmod.assert_called_once()
      os.unlink.assert_called_once()

  @patch('view.PopupView.PopupManager.show_error_popup')
  @patch('traceback.print_exc')
  def test_on_rm_error_exception(self,  mock_popup, mock_traceback):
      mock_popup = Mock()
      mock_traceback = Mock()
      os.chmod = Mock(side_effect=Exception('test'))
      os.unlink = Mock()
      model = HomeModel()
      model.on_rm_error('test', 'test', 'test')
      os.chmod.assert_called_once()
      os.unlink.assert_not_called()
     


  
if __name__ == "__main__":
    unittest.main()