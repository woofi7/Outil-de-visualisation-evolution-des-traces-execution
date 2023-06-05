import unittest
from unittest.mock import Mock
from controller.TraceVisualizerController import TraceVisualizerController
from unittest.mock import MagicMock
from PyQt6.QtWidgets import QLineEdit, QApplication



class test_TraceVisualizerController(unittest.TestCase):
        
    
    def test_ok_button_clicked(self):
        app = QApplication([])
        view = Mock()
        model = Mock()
        home_view = Mock()
        home_view.repoList.currentText = MagicMock(return_value='test')
        model.getCommitChanges = MagicMock(return_value = [['test', 'test', 'test', 'test']] )
        tvc = TraceVisualizerController(view, model, home_view)
        tvc.show_commit_changes(QLineEdit('test: test: test: test, File: '))
        self.assertIsNotNone(tvc.CommitWindowView)
        view.commit_windows.append.assert_called_once()
   

if __name__ == "__main__":
    unittest.main()