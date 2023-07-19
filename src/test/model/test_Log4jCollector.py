import unittest

from model.LogInstructionCollectors.Log4jCollector import Log4jCollector
from pydriller import Repository, Commit, ModificationType
from datetime import datetime
from PyQt6.QtWidgets import QApplication
from unittest.mock import MagicMock


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
        self.assertEqual(len(deleted_logs), 0)

    def test_get_log_instructions(self):
        app = QApplication([])
        # Mocked commit objects
        commit1 = MagicMock()
        commit1.author = "John"
        commit1.modified_files = [
            MagicMock(filename="file1.java", old_path=None, new_path="dir/file1.java", change_type=ModificationType.ADD),
            MagicMock(filename="file2.java", old_path=None, new_path="dir/file2.java", change_type=ModificationType.ADD),
        ]

        commit2 = MagicMock()
        commit2.author = "Jane"
        commit2.modified_files = [
            MagicMock(filename="file1.java", old_path="dir/file1.java", new_path="dir/file1_updated.java", change_type=ModificationType.RENAME),
            MagicMock(filename="file3.java", old_path=None, new_path="dir/file3.java", change_type=ModificationType.ADD),
        ]

        commit3 = MagicMock()
        commit3.author = "Jane"
        commit3.modified_files = [
            MagicMock(filename="file1_updated.java", old_path="dir/file1_updated.java", new_path="", change_type=ModificationType.DELETE),
        ]

        # Mock the Repository class and its methods
        repository_mock = MagicMock()
        Repository.traverse_commits=  MagicMock(return_value = [commit1, commit2, commit3])

        # Instantiate the class under test
        my_object = Log4jCollector()
        my_object.getLogs = MagicMock(return_value=([],[]))

        # Call the method to be tested
        result_logs, result_deleted_logs = my_object.get_log_instructions(
            repo="my_repo",
            from_date=datetime(2022, 1, 1),
            to_date=datetime(2022, 12, 31),
            path_in_directory="",
            branch="master",
            author="",
        )

        # Perform assertions on the results
        expected_logs = {
            "dir/file1.java": [],
            "dir/file2.java": [],
            "dir/file1_updated.java": [],
            "dir/file3.java": [],
        }
        expected_deleted_logs = [[],[],[]]
        self.assertEqual(result_logs, expected_logs)
        self.assertEqual(result_deleted_logs, expected_deleted_logs)

        
if __name__ == "__main__":
    unittest.main()