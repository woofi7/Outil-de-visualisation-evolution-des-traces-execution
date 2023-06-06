import unittest
from model.DataModel import DataModel
from model.GlobalModel import GlobalModel


class TestGlobalModel(unittest.TestCase):
        
    def setUp(self):
        self.model = GlobalModel()
        
    # getRepo()
    def test_getRepo_existingRepo(self):
        self.model.addRepoBranch("repo1", "branch1")
        self.model.addRepoBranch("repo1", "branch2")
        self.assertEqual(self.model.getRepo("repo1"), {"branch1": DataModel("repo1", "branch1"), "branch2": DataModel("repo1", "branch2")})

    def test_getRepo_nonExistingRepo(self):
        with self.assertRaises(ValueError):
            self.model.getRepo("repo1")
    
    # getRepoBranch()
    def test_getRepoBranch_existingRepo_existingBranch(self):
        self.model.addRepoBranch("repo1", "branch1")
        self.assertEqual(self.model.getRepoBranch("repo1", "branch1"), DataModel("repo1", "branch1"))

    def test_getRepoBranch_existingRepo_nonExistingBranch(self):
        self.model.addRepoBranch("repo1", "branch1")
        with self.assertRaises(ValueError):
            self.model.getRepoBranch("repo1", "branch2")

    def test_getRepoBranch_nonExistingRepo(self):
        with self.assertRaises(ValueError):
            self.model.getRepoBranch("repo1", "branch1")

    # addRepoBranch()
    def test_addRepoBranch_newRepo_newBranch(self):
        self.model.addRepoBranch("repo1", "branch1")
        self.assertEqual(self.model.getRepo("repo1"), {"branch1": DataModel("repo1", "branch1")})

    def test_addRepoBranch_existingRepo_newBranch(self):
        self.model.addRepoBranch("repo1", "branch1")
        self.model.addRepoBranch("repo1", "branch2")
        self.assertEqual(self.model.getRepo("repo1"), {"branch1": DataModel("repo1", "branch1"), "branch2": DataModel("repo1", "branch2")})

    def test_addRepoBranch_existingRepo_existingBranch(self):
        self.model.addRepoBranch("repo1", "branch1")
        with self.assertRaises(ValueError):
            self.model.addRepoBranch("repo1", "branch1")
            
    # removeRepo()
    def test_removeRepo_existingRepo(self):
        self.model.addRepoBranch("repo1", "branch1")
        self.model.addRepoBranch("repo1", "branch2")
        self.model.addRepoBranch("repo2", "branch1")
        self.model.removeRepo("repo1")
        with self.assertRaises(ValueError):
            self.model.getRepo("repo1")
        self.assertEqual(self.model.getRepo("repo2"), {"branch1": DataModel("repo2", "branch1")})
    
    def test_removeRepo_nonExistingRepo(self):
        self.model.addRepoBranch("repo1", "branch1")
        self.model.addRepoBranch("repo1", "branch2")
        self.model.addRepoBranch("repo2", "branch1")
        with self.assertRaises(ValueError):
            self.model.removeRepo("repo3")
    
    # removeRepoBranch()
    def test_removeRepo_nonExistingRepo(self):
        self.model.addRepoBranch("repo1", "branch1")
        self.model.addRepoBranch("repo1", "branch2")
        self.model.addRepoBranch("repo2", "branch1")
        with self.assertRaises(ValueError):
            self.model.removeRepo("repo3")
    
    def test_removeRepoBranch_existingBranch(self):
        self.model.addRepoBranch("repo1", "branch1")
        self.model.addRepoBranch("repo1", "branch2")
        self.model.addRepoBranch("repo2", "branch1")
        self.model.removeRepoBranch("repo1", "branch1")
        with self.assertRaises(ValueError):
            self.model.getRepoBranch("repo1", "branch1")
        self.assertEqual(self.model.getRepo("repo1"), {"branch2": DataModel("repo1", "branch2")})
    
    def test_removeRepoBranch_nonExistingBranch(self):
        self.model.addRepoBranch("repo1", "branch1")
        self.model.addRepoBranch("repo1", "branch2")
        self.model.addRepoBranch("repo2", "branch1")
        with self.assertRaises(ValueError):
            self.model.removeRepoBranch("repo1", "branch3")

if __name__ == "__main__":
    unittest.main()
