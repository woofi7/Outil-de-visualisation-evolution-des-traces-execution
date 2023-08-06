import unittest
from unittest.mock import patch, MagicMock, Mock
from datetime import datetime
from pydriller import Repository
from pydriller.domain.commit import ModificationType
from model.LogInstructionCollectors.LogInstructionCollector import LogInstructionCollector
from model.LogInstructionCollectors.LogInstruction import LogInstruction
from model.LogInstructionCollectors.Modification import Modification
from model.LogInstructionCollectors.Log4pCollector import Log4pCollector

class Log4pCollectorTestCase(unittest.TestCase):
    def test_get_log_instructions(self):

        # Mocked commit objects
        commit1 = MagicMock()
        commit1.author.name = "John"
        commit1.parents = []
        commit1.diff.return_value = [
            MagicMock(change_type='A', a_path=None, b_path="dir/file1.py"),
            MagicMock(change_type='A', a_path=None, b_path="dir/file2.py"),
        ]

        commit2 = MagicMock()
        commit2.author.name = "Jane"
        commit2.parents = [commit1]
        commit2.diff.return_value = [
            MagicMock(change_type='R', a_path="dir/file1.py", b_path="dir/file1_updated.py"),
            MagicMock(change_type='A', a_path=None, b_path="dir/file3.py"),
        ]

        commit3 = MagicMock()
        commit3.author.name = "Jane"
        commit3.parents = [commit2]
        commit3.diff.return_value = [
            MagicMock(change_type='R', a_path="dir/file1.py", b_path="dir/file1_updated.py"),
            MagicMock(change_type='D', a_path="dir/file1_updated.py", b_path=None),
        ]

        # Patch the git.Repo class
        with patch('model.ReposManager.ReposManager.get_repo_branch')as repo_mock, \
                patch('model.LogInstructionCollectors.Log4pCollector.Log4pCollector.getLogs') as getLogs_mock:
            # Configure repo_mock and set its behavior
            repo_instance = Mock()
            branch_ref = Mock()
            repo_mock.return_value = (repo_instance, branch_ref)

            repo_instance.iter_commits.return_value = [commit1, commit2, commit3]

            # Instantiate the class under test
            my_object = Log4pCollector()
            logInstruction = LogInstruction('info','"info"', [], '2023-01-01')     
            logInstruction1 = LogInstruction('info','"info"', [], '2023-01-01')

            getLogs_mock.return_value=([logInstruction], [logInstruction1])

            # Call the method to be tested
            result_logs = my_object.get_log_instructions(
                repo_path="my_repo",
                from_date=datetime(2022, 1, 1),
                to_date=datetime(2022, 12, 31),
                path_in_directory="",
                branch="master",
                author=""
            )
    
            self.assertEqual(len(result_logs), 6)
            getLogs_mock.assert_called()
    def test_logs_empty(self):
        beforeCode = None
        afterCode = None
        self.strat = Log4pCollector()
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=[], type='MODIFY', author='test')
        self.assertEqual(logs, [])
        self.assertEqual(deleted_logs, [])

    def test_getLogs_untouched(self):
        beforeCode = """import log4p
                        
logger.info('test1')
                        
logger.info('test2')"""

        afterCode = """import log4p
                        
logger.info('test1')
                        
logger.info('test2')"""
        self.strat = Log4pCollector()
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=[], type='test', author='test')
        self.assertEqual(len(logs), 2)
        self.assertEqual(logs[0].instruction, '"""test1"""')
        self.assertEqual(deleted_logs, [])

    def test_getLogs_matched(self):
        beforeCode = ""

        afterCode = """import log4p
                        
logger.info('test1')
                        
logger.info('test2')"""
        self.strat = Log4pCollector()
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=[], type='test', author='test')
        beforeCode = """import log4p
                        
logger.info('test1')
                        
logger.info('test2')"""

        afterCode = """import log4p
                        
logger.info('test1')
                        
logger.info('test2')"""
        self.strat = Log4pCollector()
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=logs, type='test', author='test')
        self.assertEqual(len(logs), 2)
        self.assertEqual(logs[0].instruction, '"""test1"""')
        self.assertEqual(deleted_logs, [])

    def test_getLogs_modified(self):
        beforeCode = ""

        afterCode = """import log4p
                        
logger.info('test1')
                        
logger.info('test2')"""
        self.strat = Log4pCollector()
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=[], type='test', author='test')
        beforeCode = """import log4p
                        
logger.info('test1')
                        
logger.info('test2')"""

        afterCode = """import log4p
                        
logger.info('test1')
                        
logger.info('test3')"""
        self.strat = Log4pCollector()
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=logs, type='test', author='test')
        self.assertEqual(len(logs), 2)
        self.assertEqual(logs[1].instruction, '"""test3"""')
        self.assertEqual(deleted_logs, [])

    def test_getLogs_remove_log4p(self):
        beforeCode = ""

        afterCode = """import log4p
                        
logger.info('test1')
                        
logger.info('test2')"""
        self.strat = Log4pCollector()
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=[], type='test', author='test')
        beforeCode = """import log4p
                        
logger.info('test1')
                        
logger.info('test2')"""

        afterCode = """
                        
logger.info('test1')
                        
logger.info('test3')"""
        self.strat = Log4pCollector()
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=logs, type='test', author='test')
        self.assertEqual(logs, [])
        self.assertEqual(len(deleted_logs), 2)

    def test_getLogs_modified_complex(self):
        beforeCode = ""

        afterCode = """import log4p
               
def test(self):    
  while(True):     
    logger.info('test1')
                        
    logger.info('test2')"""
        self.strat = Log4pCollector()
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=[], type='test', author='test')
        self.assertEqual(len(logs), 2)
        self.assertEqual(logs[1].instruction, '"""test2"""')
        self.assertEqual(deleted_logs, [])

if __name__ == '__main__':
    unittest.main()
