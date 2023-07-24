import unittest
from unittest.mock import Mock
from view.SelectCommitWindowView import SelectCommitWindowView
from PyQt6.QtWidgets import QApplication, QListWidget, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest


class test_SelectCommitWindowView(unittest.TestCase):
        
    
  def test_CommitWindowView_Init(self):
     app = QApplication([])
    #  scwv = SelectCommitWindowView([['test','test','test','test','test'],['test','test','test','test','test'],['test','test','test','test','test'],['test','test','test','test','test'],['test','test','test','test','test']])
    #  self.assertIsNotNone(scwv.commit_list)
     commit_changes = [['test', 'test', 'test', 'test', 'test'],
                          ['test', 'test', 'test', 'test', 'test'],
                          ['test', 'test', 'test', 'test', 'test'],
                          ['test', 'test', 'test', 'test', 'test'],
                          ['test', 'test', 'test', 'test', 'test']]
     scwv = SelectCommitWindowView(commit_changes)

    # Simulate a button click
     select_button = scwv.findChild(QPushButton, "Select")
     #QTest.mouseClick(select_button, Qt.MouseButton.LeftButton)

     scwv.handleSelect()

     # Check if CommitWindowView was created with the correct data
     selected_item = scwv.commit_list.currentItem()
     if selected_item:
         selected_commit = selected_item.data(Qt.ItemDataRole.UserRole)

            # Here, you can add your specific assertions based on the expected data.
            # For example, if you know the first item in commit_changes is ['test', 'test', 'test', 'test', 'test'],
            # you can check if selected_commit matches this data.
         self.assertEqual(selected_commit, ['test', 'test', 'test', 'test', 'test'])

        # You may also want to add assertions to check if the CommitWindowView is displayed properly, but that would depend
        # on the behavior of CommitWindowView and whether you want to test its display or not.

        # Clean up the application event loop
     app.exit()

if __name__ == "__main__":
    unittest.main()