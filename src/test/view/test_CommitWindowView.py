import unittest
from model.NewRepoModel import NewRepoModel
from unittest.mock import Mock
from view.CommitWindowView import CommitWindowView
from PyQt6.QtWidgets import QApplication



class test_CommitWindowView(unittest.TestCase):
        
    
  def test_CommitWindowView_Init(self):
     app = QApplication([])
     cwv = CommitWindowView([['test','test','test','test']])
     self.assertIsNotNone(cwv.code_tables)
     self.assertIsNotNone(cwv.code_table)

if __name__ == "__main__":
    unittest.main()