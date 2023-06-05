import unittest
from model.NewRepoModel import NewRepoModel
from unittest.mock import Mock
from git import Repo



class test_NewRepoModel(unittest.TestCase):
        
    
  def test_cloneRepo_existing_repo(self):
     newRepoModel = NewRepoModel()
     Repo.clone_from = Mock()
     newRepoModel.cloneRepo('respoUrl','./test/model/test_NewRepoModel.py')
     Repo.clone_from.assert_not_called()

  def test_cloneRepo_not_existing_repo(self):
     newRepoModel = NewRepoModel()
     Repo.clone_from = Mock()
     newRepoModel.cloneRepo('respoUrl','./test/test/test_NewRepoModel.py')
     Repo.clone_from.assert_called_once_with('respoUrl','./test/test/test_NewRepoModel.py')


if __name__ == "__main__":
    unittest.main()