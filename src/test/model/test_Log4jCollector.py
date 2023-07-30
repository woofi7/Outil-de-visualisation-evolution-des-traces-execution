import unittest

from model.LogInstructionCollectors.Log4jCollector import Log4jCollector
from pydriller import Repository, Commit, ModificationType
from datetime import datetime
from git import Repo, Diff
from PyQt6.QtWidgets import QApplication
from unittest.mock import MagicMock, patch, Mock
from model.LogInstructionCollectors.LogInstruction import LogInstruction


class TestStrategyLog4j(unittest.TestCase):
        
    def setUp(self):
        self.strat = Log4jCollector()

    def test_logs_empty(self):
        beforeCode = None
        afterCode = None
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=[], type='test', author='test')
        self.assertEqual(logs, [])
        self.assertEqual(deleted_logs, [])
    
    def test_getLogs_untouched(self):
        beforeCode = """import log4j;
                        public class Test {
                        public Test() {
                        logger.info('test1');
                        logger.info('test2');}}"""
        afterCode = """import log4j;
                        public class Test {
                        public Test() {
                        logger.info('test1');
                        logger.info('test2');}}"""
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=[], type='test', author='test')
        self.assertEqual(len(logs), 2)
        self.assertEqual(logs[0].instruction, "'test1'")
        self.assertEqual(deleted_logs, [])
        
    def test_logs_modified(self):
        beforeCode = ""
        afterCode = '''import log4j;
                        public class Test {
                        public Test() {
                        logger.info("test1");
                        logger.info("test2");}}'''
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=[], type='test', author='test')
        self.assertEqual(len(logs), 2)
        self.assertEqual(len(deleted_logs), 0)

        beforeCode = '''import log4j;
                        public class Test {
                        public Test() {
                        logger.info("test1");
                        logger.info("test2");}}'''
        afterCode = '''import log4j;
                        public class Test {
                        public Test() {
                       logger.warn("test1");
                       logger.info("test2");}}'''
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=logs, type='test', author='test')
        self.assertEqual(len(logs), 2)
        self.assertEqual(len(deleted_logs), 0)

    def test_logs_modified_remove_log4j(self):
        beforeCode = ""
        afterCode = '''import log4j;
                        public class Test {
                        public Test() {
                        logger.info("test1");
                        logger.info("test2");}}'''
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=[], type='test', author='test')
        self.assertEqual(len(logs), 2)
        self.assertEqual(len(deleted_logs), 0)

        beforeCode = '''import log4j;
                        public class Test {
                        public Test() {
                        logger.info("test1");
                        logger.info("test2");}}'''
        afterCode = '''
                        public class Test {
                        public Test() {
                       logger.warn("test1");
                       logger.info("test2");}}'''
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=logs, type='test', author='test')
        self.assertEqual(logs, [])
        self.assertEqual(len(deleted_logs), 2)
        
    def test_logs_deleted(self):
        beforeCode = ""
        afterCode = '''import log4j;
                        public class Test {
                        public Test() {
                        logger.info("test1");
                        logger.info("test2");}}'''
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=[], type='test', author='test')
        self.assertEqual(len(logs), 2)
        self.assertEqual(len(deleted_logs), 0)

        beforeCode = '''import log4j;
                        public class Test {
                        public Test() {
                        logger.info("test1");
                        logger.info("test2");}}'''
        afterCode = '''import log4j;
                        public class Test {
                        public Test() {}}'''
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=logs, type='test', author='test')
        self.assertEqual(len(logs), 0)
        self.assertEqual(len(deleted_logs), 2)

        
    
        
    def test_getLogs_deleted(self):
        beforeCode = ""
        afterCode = """import log4j;
                        public class Test {
                        public Test() {
                        logger.error("message");
                        //java code ici, java code là
                        warn.info('test1');
                        logger.info('test2');}}"""
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=[], type='test', author='test')
        self.assertEqual(len(logs), 3)
        self.assertEqual(len(deleted_logs), 0)

        beforeCode = """import log4j;
                        public class Test {
                        public Test() {
                        logger.error("message");
                        //java code ici, java code là
                        warn.info('test1');
                        logger.info('test2');}}"""
        afterCode = """import log4j;
                        public class Test {
                        public Test() {
                        logger.info('test3');}}"""
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=logs, type='test', author='test')
        self.assertEqual(len(logs), 1)
        self.assertEqual(len(deleted_logs), 2)
        self.assertEqual(len(logs[0].modifications), 2)
        
    def test_complex_logs(self):
        logs = []
        beforeCode = ''
        afterCode = '''import org.apache.log4j.Logger;

                        public class Test {
                            private static final Logger logger = Logger.getLogger(Test.class);

                            public Test(String[] files) {
                                logger.info("Starting processing");
                                logger.debug("Configuration loaded successfully");
                                for (String file : files) {
                                    logger.info("Processing file: " + file);
                                    logger.fatal("Processing file: " + file);
                                    try {
                                        //process_file(file);
                                        logger.info("File " + file + " processed successfully");
                                    } catch (Exception e) {
                                        logger.error("Error while processing file " + file + ": " + e);
                                    }
                                }
                                logger.info("Processing finished");
                            }
                        }'''
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=logs, type='test', author='test')
        self.assertEqual(len(logs), 7)
        self.assertEqual(len(deleted_logs), 0)


        beforeCode = '''import org.apache.log4j.Logger;

                        public class Test {
                            private static final Logger logger = Logger.getLogger(Test.class);

                            public Test(String[] files) {
                                logger.info("Starting processing");
                                logger.debug("Configuration loaded successfully");
                                for (String file : files) {
                                    logger.info("Processing file: " + file,(NullPointerException) new NullPointerException("Null pointer exception"));
                                    logger.fatal("Processing file: " + file);
                                    try {
                                        //process_file(file);
                                        logger.info("File " + file + " processed successfully");
                                    } catch (Exception e) {
                                        logger.error("Error while processing file " + file + ": " + e);
                                    }
                                }
                                logger.info("Processing finished");
                            }
                        }'''
        afterCode = '''import org.apache.log4j.Logger;

                        public class Test {
                            private static final Logger logger = Logger.getLogger(Test.class);

                            public Test(String[] files) {
                                logger.info("Starting processing");
                                logger.debug("Configuration loaded successfully", (NullPointerException)new NullPointerException("Null pointer exception"));
                                for (String file : files) {
                                    logger.info("Processing file: " + file);
                                    logger.fatal("Processing file: " + file);
                                    try {
                                        //process_file(file);
                                    } catch (Exception e) {
                                        logger.error(logger.equals("null")	+"Error while processing file " + file + ": " + e);
                                    }
                                }
                                logger.info("Processing finished");
                            }
                        }'''
        logs, deleted_logs = self.strat.getLogs(hash='test', filename='testFile',before_code=beforeCode, after_code=afterCode, date='2023-01-01',logs=logs, type='test', author='test')
        self.assertEqual(len(logs), 6)

    def test_get_log_instructions(self):
        app = QApplication([])

        # Mocked commit objects
        commit1 = MagicMock()
        commit1.author.name = "John"
        commit1.parents = []
        commit1.diff.return_value = [
            MagicMock(change_type='A', a_path=None, b_path="dir/file1.java"),
            MagicMock(change_type='A', a_path=None, b_path="dir/file2.java"),
        ]

        commit2 = MagicMock()
        commit2.author.name = "Jane"
        commit2.parents = [commit1]
        commit2.diff.return_value = [
            MagicMock(change_type='R', a_path="dir/file1.java", b_path="dir/file1_updated.java"),
            MagicMock(change_type='A', a_path=None, b_path="dir/file3.java"),
        ]

        commit3 = MagicMock()
        commit3.author.name = "Jane"
        commit3.parents = [commit2]
        commit3.diff.return_value = [
            MagicMock(change_type='R', a_path="dir/file1.java", b_path="dir/file1_updated.java"),
            MagicMock(change_type='D', a_path="dir/file1_updated.java", b_path=None),
        ]

        # Patch the git.Repo class
        with patch('model.ReposManager.ReposManager.get_repo_branch')as repo_mock, \
                patch('model.LogInstructionCollectors.Log4jCollector.Log4jCollector.getLogs') as getLogs_mock:
            # Configure repo_mock and set its behavior
            repo_instance = Mock()
            branch_ref = Mock()
            repo_mock.return_value = (repo_instance, branch_ref)

            repo_instance.iter_commits.return_value = [commit1, commit2, commit3]

            # Instantiate the class under test
            my_object = Log4jCollector()
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

        
if __name__ == "__main__":
    unittest.main()