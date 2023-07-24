import unittest
from unittest.mock import Mock
from view.SelectCommitWindowView import SelectCommitWindowView
from PyQt6.QtWidgets import QApplication



class test_SelectCommitWindowView(unittest.TestCase):
        
    
  def test_CommitWindowView_Init(self):
     app = QApplication([])
     cwv = SelectCommitWindowView([['test','test','test','test'],'test','test','test','test'])
     self.assertIsNotNone(cwv.code_tables)
     self.assertIsNotNone(cwv.code_table)

if __name__ == "__main__":
    unittest.main()