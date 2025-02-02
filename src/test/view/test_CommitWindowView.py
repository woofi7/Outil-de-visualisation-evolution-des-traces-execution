import unittest
from unittest.mock import Mock
from view.CommitWindowView import CommitWindowView
from PyQt6.QtWidgets import QApplication



class test_CommitWindowView(unittest.TestCase):
  
  @classmethod
  def setUpClass(cls):
      cls.app = QApplication([])
        
  def test_CommitWindowView_Init(self):
     cwv = CommitWindowView([['test','test','test','test'],'test','test','test'])
     self.assertIsNotNone(cwv.code_tables)
     self.assertIsNotNone(cwv.code_table)

if __name__ == "__main__":
    unittest.main()