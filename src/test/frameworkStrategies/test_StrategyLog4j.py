import unittest

from frameworkStrategies.StrategyLog4j import StrategyLog4j


class TestStrategyLog4j(unittest.TestCase):
        
    def setUp(self):
        self.strat = StrategyLog4j()
        
    def test_logs_empty(self):
        beforeCode = ""
        afterCode = ""
        logs = self.strat.getLogs(beforeCode=beforeCode, afterCode=afterCode)
        self.assertEqual(logs, None)
    
    def test_getLogs_untouched(self):
        beforeCode = """import log4j;
                        logger.info('test1');
                        logger.info('test2');"""
        afterCode = """import log4j;
                        logger.info('test1');
                        logger.info('test2');"""
        logs = self.strat.getLogs(beforeCode=beforeCode, afterCode=afterCode)
        
        self.assertEqual(len(logs["deletedLogs"]), 0)
        self.assertEqual(len(logs["untouchedLogs"]), 2)
        self.assertEqual(len(logs["modifiedLogs"]), 0)
        self.assertEqual(len(logs["addedLogs"]), 0)
        
    def test_logs_modified(self):
        beforeCode = '''import log4j;
                        logger.info("test1");
                        logger.info("test2");'''
        afterCode = '''import log4j;
                       logger.warn("test3");
                       logger.info("test2");'''
        logs = self.strat.getLogs(beforeCode=beforeCode, afterCode=afterCode)
        self.assertEqual(len(logs["deletedLogs"]), 1)
        self.assertEqual(len(logs["untouchedLogs"]), 1)
        self.assertEqual(len(logs["modifiedLogs"]), 0)
        self.assertEqual(len(logs["addedLogs"]), 1)
        
    def test_logs_deleted(self):
        beforeCode = '''import log4j;
                        logger.info("test1");
                        logger.info("test2");'''
        afterCode = '''import log4j;
                       logger.info("test1");'''
        logs = self.strat.getLogs(beforeCode=beforeCode, afterCode=afterCode)
        self.assertEqual(len(logs["deletedLogs"]), 1)
        self.assertEqual(len(logs["untouchedLogs"]), 1)
        self.assertEqual(len(logs["modifiedLogs"]), 0)
        self.assertEqual(len(logs["addedLogs"]), 0)
        
    
        
    def test_getLogs_deleted(self):
        beforeCode = """import log4j;
                        logger.error("message");
                        java code ici, java code là
                        warn.info('test1');
                        logger.info('test2');"""
        afterCode = """import log4j;
                        logger.info('test3');"""
        logs = self.strat.getLogs(beforeCode=beforeCode, afterCode=afterCode)
        
        self.assertEqual(len(logs["deletedLogs"]), 2)
        self.assertEqual(len(logs["untouchedLogs"]), 0)
        self.assertEqual(len(logs["modifiedLogs"]), 1)
        self.assertEqual(len(logs["addedLogs"]), 0)
        
    def test_complex_logs(self):
        beforeCode = '''import log4j;
                        logger.info("Starting processing");
                        logger.debug("Configuration loaded successfully");
                        for file in files:
                            logger.info("Processing file: %s", file);
                            logger.fatal("Processing file: %s", file);
                            try:
                                process_file(file);
                                logger.info("File %s processed successfully", file);
                            except Exception as e:
                                logger.error("Error while processing file %s: %s", file, e);
                        logger.info("Processing finished");'''
        afterCode = '''import log4j;
                       logger.info("Starting processing");
                       logger.debug("Configuration loaded successfully");
                       for file in files:
                           logger.info("Processing file: %s", file);
                           try:
                               process_file(file);
                               logger.info("File %s processed successfully", file);
                           except ValueError as ve:
                               logger.error("Error while processing file %s: %s", file, e);
                           except Exception as e:
                               logger.warn("Invalid file %s: %s", file, ve);
                       logger.info("Processing finished");'''
        logs = self.strat.getLogs(beforeCode=beforeCode, afterCode=afterCode)
        self.assertEqual(len(logs["deletedLogs"]), 1)
        self.assertEqual(len(logs["untouchedLogs"]), 6)
        self.assertEqual(len(logs["modifiedLogs"]), 0)
        self.assertEqual(len(logs["addedLogs"]), 1)
        
if __name__ == "__main__":
    unittest.main()