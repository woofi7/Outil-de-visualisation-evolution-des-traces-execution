import unittest
from model.DataModel import DataModel
from model.GlobalModel import GlobalModel
from model.Instructions import Instructions
from PyQt6.QtWidgets import QApplication
from pydriller import Repository
from unittest.mock import MagicMock


class TestGlobalModel(unittest.TestCase):
        
    def setUp(self):
        self.model = GlobalModel()
        self.instruction =  Instructions("./test/test/test_HomeController.py", ['2023-01-01', '2023-02-01'], ['log4j'], [])


        
    # getRepo()
    def test_getRepo_existingRepo(self):
        self.model.addRepoBranch("repo1", "branch1", self.instruction)
        self.model.addRepoBranch("repo1", "branch2", self.instruction)
        Repository.traverse_commits = MagicMock(return_value=[])
        self.assertEqual(self.model.getRepo("repo1"), {"branch1": DataModel("repo1", "branch1", self.instruction), "branch2": DataModel("repo1", "branch2", self.instruction)})

    def test_getRepo_nonExistingRepo(self):
        with self.assertRaises(ValueError):
            self.model.getRepo("repo1")
    
    # getRepoBranch()
    def test_getRepoBranch_existingRepo_existingBranch(self):
        Repository.traverse_commits = MagicMock(return_value=[])
        self.model.addRepoBranch("repo1", "branch1", self.instruction)
        self.assertEqual(self.model.getRepoBranch("repo1", "branch1"), DataModel("repo1", "branch1", self.instruction))

    def test_getRepoBranch_existingRepo_nonExistingBranch(self):
        Repository.traverse_commits = MagicMock(return_value=[])
        self.model.addRepoBranch("repo1", "branch1", self.instruction)
        with self.assertRaises(ValueError):
            self.model.getRepoBranch("repo1", "branch2")

    def test_getRepoBranch_nonExistingRepo(self):
        Repository.traverse_commits = MagicMock(return_value=[])
        with self.assertRaises(ValueError):
            self.model.getRepoBranch("repo1", "branch1")

    # addRepoBranch()
    def test_addRepoBranch_newRepo_newBranch(self):
        Repository.traverse_commits = MagicMock(return_value=[])
        self.model.addRepoBranch("repo1", "branch1", self.instruction)
        self.assertEqual(self.model.getRepo("repo1"), {"branch1": DataModel("repo1", "branch1", self.instruction)})

    def test_addRepoBranch_existingRepo_newBranch(self):
        Repository.traverse_commits = MagicMock(return_value=[])
        self.model.addRepoBranch("repo1", "branch1", self.instruction)
        self.model.addRepoBranch("repo1", "branch2", self.instruction)
        self.assertEqual(self.model.getRepo("repo1"), {"branch1": DataModel("repo1", "branch1", self.instruction), "branch2": DataModel("repo1", "branch2", self.instruction)})

    def test_addRepoBranch_existingRepo_existingBranch(self):
        Repository.traverse_commits = MagicMock(return_value=[])
        self.model.addRepoBranch("repo1", "branch1", self.instruction)
        with self.assertRaises(ValueError):
            self.model.addRepoBranch("repo1", "branch1", self.instruction)
            
    # removeRepo()
    def test_removeRepo_existingRepo(self):
        Repository.traverse_commits = MagicMock(return_value=[])
        self.model.addRepoBranch("repo1", "branch1", self.instruction)
        self.model.addRepoBranch("repo1", "branch2", self.instruction)
        self.model.addRepoBranch("repo2", "branch1", self.instruction)
        self.model.removeRepo("repo1")
        with self.assertRaises(ValueError):
            self.model.getRepo("repo1")
        self.assertEqual(self.model.getRepo("repo2"), {"branch1": DataModel("repo2", "branch1", self.instruction)})
    
    def test_removeRepo_nonExistingRepo(self):
        Repository.traverse_commits = MagicMock(return_value=[])
        self.model.addRepoBranch("repo1", "branch1", self.instruction)
        self.model.addRepoBranch("repo1", "branch2", self.instruction)
        self.model.addRepoBranch("repo2", "branch1", self.instruction)
        with self.assertRaises(ValueError):
            self.model.removeRepo("repo3")
    
    # removeRepoBranch()
    def test_removeRepo_nonExistingRepo(self):
        Repository.traverse_commits = MagicMock(return_value=[])
        self.model.addRepoBranch("repo1", "branch1", self.instruction)
        self.model.addRepoBranch("repo1", "branch2", self.instruction)
        self.model.addRepoBranch("repo2", "branch1", self.instruction)
        with self.assertRaises(ValueError):
            self.model.removeRepo("repo3")
    
    def test_removeRepoBranch_existingBranch(self):
        Repository.traverse_commits = MagicMock(return_value=[])
        self.model.addRepoBranch("repo1", "branch1", self.instruction)
        self.model.addRepoBranch("repo1", "branch2", self.instruction)
        self.model.addRepoBranch("repo2", "branch1", self.instruction)
        self.model.removeRepoBranch("repo1", "branch1")
        with self.assertRaises(ValueError):
            self.model.getRepoBranch("repo1", "branch1")
        self.assertEqual(self.model.getRepo("repo1"), {"branch2": DataModel("repo1", "branch2", self.instruction)})
    
    def test_removeRepoBranch_nonExistingBranch(self):
        Repository.traverse_commits = MagicMock(return_value=[])
        self.model.addRepoBranch("repo1", "branch1", self.instruction)
        self.model.addRepoBranch("repo1", "branch2", self.instruction)
        self.model.addRepoBranch("repo2", "branch1", self.instruction)
        with self.assertRaises(ValueError):
            self.model.removeRepoBranch("repo1", "branch3")

if __name__ == "__main__":
    unittest.main()
