import os
import unittest
from unittest.mock import patch, Mock
from model.ReposManager import ReposManager

class TestReposManager(unittest.TestCase):
    @patch('os.scandir')
    def test_get_repos(self, mock_scandir):
        mock_dir_entry = Mock()
        mock_dir_entry.is_dir.return_value = True
        mock_dir_entry.name = 'test_repo'
        mock_scandir.return_value = [mock_dir_entry]

        repos_manager = ReposManager()
        repos = repos_manager.get_repos('/path/to/repos')

        mock_scandir.assert_called_once_with('/path/to/repos')
        self.assertEqual(repos, ['test_repo'])

    @patch('git.Repo')
    def test_git_pull(self, mock_repo):
        mock_repo_instance = Mock()
        mock_repo.return_value = mock_repo_instance

        repos_manager = ReposManager()
        repos_manager.git_pull('/path/to/repo')

        mock_repo.assert_called_once_with('/path/to/repo')
        mock_repo_instance.remotes.origin.pull.assert_called_once()

    @patch('git.Repo.clone_from')
    def test_clone_repo(self, mock_clone_from):
        repos_manager = ReposManager()
        repos_manager.clone_repo('https://url.to/repo.git', '/path/to/repo')

        mock_clone_from.assert_called_once_with('https://url.to/repo.git', '/path/to/repo')

if __name__ == "__main__":
    unittest.main()
