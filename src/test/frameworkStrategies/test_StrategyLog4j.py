import unittest

from frameworkStrategies.StrategyLog4j import StrategyLog4j


class TestStrategyLog4j(unittest.TestCase):
        
    def setUp(self):
        self.strat = StrategyLog4j()
        
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
        
    def test_getLogs_deleted(self):
        beforeCode = """import log4j;
                        logger.info('test1');
                        logger.info('test2');"""
        afterCode = """import log4j;
                        logger.info('test3');"""
        logs = self.strat.getLogs(beforeCode=beforeCode, afterCode=afterCode)
        
        self.assertEqual(len(logs["deletedLogs"]), 1)
        self.assertEqual(len(logs["untouchedLogs"]), 0)
        self.assertEqual(len(logs["modifiedLogs"]), 1)
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
        
if __name__ == "__main__":
    unittest.main()