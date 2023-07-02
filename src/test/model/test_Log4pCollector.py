import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from pydriller import Repository
from pydriller.domain.commit import ModificationType
from model.LogInstructionCollectors.LogInstructionCollector import LogInstructionCollector
from model.LogInstructionCollectors.LogInstruction import LogInstruction
from model.LogInstructionCollectors.Modification import Modification
from model.LogInstructionCollectors.Log4pCollector import Log4pCollector

class Log4pCollectorTestCase(unittest.TestCase):
    def test_get_log_instructions(self):

        # Create some mock commit objects
        commit1 = self.create_mock_commit(
            author='John Doe',
            before_code="""import log4p
                        
log4p.info("Info message")""",
            after_code="""import log4p
                        
log4p.debug("After code")""",
            modifications_type=ModificationType.MODIFY,
            filename='src/file2.py',
            old_path='src/file2.py',
            new_path='src/file2.py'
        )
        commit2 = self.create_mock_commit(
            author='Jane Smith',
            before_code='''import log4p
                        
log4p.info("Info message")
            ''',
            after_code='x = 10',
            modifications_type=ModificationType.MODIFY,
            filename='src/file2.py',
            old_path='src/file2.py',
            new_path='src/file2.py'
        )
        commit3 = self.create_mock_commit(
            author='John Doe',
            before_code='''''',
            after_code='''import log4p
                        
log4p.info("Info message")
            ''',
            modifications_type=ModificationType.MODIFY,
            filename='src/file2.py',
            old_path='src/file2.py',
            new_path='src/file2.py'
        )
        commit4 = self.create_mock_commit(
            author='John Doe',
            before_code="""import log4p
                        
log4p.info("Info message")""",
            after_code="""import log4p
                        
log4p.debug("After code")""",
            modifications_type=ModificationType.RENAME,
            filename='src/file2.py',
            old_path='src/file2.py',
            new_path='src/file/file2.py'
        )
        commit5 = self.create_mock_commit(
            author='John Doe',
            before_code="""import log4p
                        
log4p.info("Info message")""",
            after_code="",
            modifications_type=ModificationType.DELETE,
            filename='src/file2.py',
            old_path='src/file2.py',
            new_path='src/file/file2.py'
        )

        Repository.traverse_commits =  MagicMock(return_value = [commit3, commit2, commit1, commit4, commit5])

        # Create an instance of Log4pCollector
        collector = Log4pCollector()

        # Call the method under test
        logs, deleted_logs = collector.get_log_instructions(
            repo='https://github.com/example/repo.git',
            from_date=datetime(2023, 1, 1),
            to_date=datetime(2023, 1, 31),
            path_in_directory='',
            branch='master',
            author='John Doe'
        )

        # Assert the expected results
        expected_logs = {
            'src/file/file2.py': [
                LogInstruction('debug', '"""After code"""', [
                    Modification('debug', '"""After code"""', datetime(2023, 1, 15), 'modified', 'log4p.debug("Before code")', 'log4p.debug("After code")', 'hash1', 'file2.py')
                ], datetime(2023, 1, 15)),
            ]
        }
        expected_deleted_logs = [[
                LogInstruction('info', '"""Info message"""', [
                    Modification('info', '"""Info message"""', datetime(2023, 1, 15), 'modified', 'log4p.info("Info message")', 'x = 10', 'hash2', 'file2.py')
                ], datetime(2023, 1, 15))]]

        self.assertEqual(logs['src/file/file2.py'][0].level, expected_logs['src/file/file2.py'][0].level)
        self.assertEqual(logs['src/file/file2.py'][0].instruction, expected_logs['src/file/file2.py'][0].instruction)
        self.assertEqual(logs['src/file2.py'], [])
        print(deleted_logs)
        self.assertEqual(deleted_logs[1][0].level, expected_deleted_logs[0][0].level)
        self.assertEqual(deleted_logs[1][0].instruction, expected_deleted_logs[0][0].instruction)

    def create_mock_commit(self, author, before_code, after_code, modifications_type, filename, old_path, new_path):
        # Create a mock commit object
        commit = MagicMock()
        commit.author = author

        # Create a mock modified file object
        modified_file = MagicMock()
        modified_file.filename = filename
        modified_file.old_path = old_path
        modified_file.new_path = new_path
        modified_file.change_type = modifications_type
        modified_file.source_code_before = before_code
        modified_file.source_code = after_code

        # Set up the commit to return the mock modified file object
        commit.modified_files = [modified_file]

        return commit
    def test_logs_empty(self):
        beforeCode = None
        afterCode = None
        self.strat = Log4pCollector()
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=[], type='MODIFY')
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
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=[], type='test')
        self.assertEqual(len(logs), 2)
        self.assertEqual(logs[0].instruction, '"""test1"""')
        self.assertEqual(deleted_logs, [])

    def test_getLogs_matched(self):
        beforeCode = ""

        afterCode = """import log4p
                        
logger.info('test1')
                        
logger.info('test2')"""
        self.strat = Log4pCollector()
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=[], type='test')
        beforeCode = """import log4p
                        
logger.info('test1')
                        
logger.info('test2')"""

        afterCode = """import log4p
                        
logger.info('test1')
                        
logger.info('test2')"""
        self.strat = Log4pCollector()
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=logs, type='test')
        self.assertEqual(len(logs), 2)
        self.assertEqual(logs[0].instruction, '"""test1"""')
        self.assertEqual(deleted_logs, [])

    def test_getLogs_modified(self):
        beforeCode = ""

        afterCode = """import log4p
                        
logger.info('test1')
                        
logger.info('test2')"""
        self.strat = Log4pCollector()
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=[], type='test')
        beforeCode = """import log4p
                        
logger.info('test1')
                        
logger.info('test2')"""

        afterCode = """import log4p
                        
logger.info('test1')
                        
logger.info('test3')"""
        self.strat = Log4pCollector()
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=logs, type='test')
        self.assertEqual(len(logs), 2)
        self.assertEqual(logs[1].instruction, '"""test3"""')
        self.assertEqual(deleted_logs, [])

    def test_getLogs_remove_log4p(self):
        beforeCode = ""

        afterCode = """import log4p
                        
logger.info('test1')
                        
logger.info('test2')"""
        self.strat = Log4pCollector()
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=[], type='test')
        beforeCode = """import log4p
                        
logger.info('test1')
                        
logger.info('test2')"""

        afterCode = """
                        
logger.info('test1')
                        
logger.info('test3')"""
        self.strat = Log4pCollector()
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=logs, type='test')
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
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=[], type='test')
        self.assertEqual(len(logs), 2)
        self.assertEqual(logs[1].instruction, '"""test2"""')
        self.assertEqual(deleted_logs, [])

if __name__ == '__main__':
    unittest.main()
