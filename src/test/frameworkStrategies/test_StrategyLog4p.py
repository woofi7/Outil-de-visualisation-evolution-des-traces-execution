import unittest

from frameworkStrategies.StrategyLog4p import StrategyLog4p


class TestStrategyLog4p(unittest.TestCase):
        
    def setUp(self):
        self.strat = StrategyLog4p()
        
    def test_logs_empty(self):
        beforeCode = ""
        afterCode = ""
        logs = self.strat.getLogs(hash='test', filename='testFile',beforeCode=beforeCode, afterCode=afterCode, date='2023-01-01',logs=[])
        self.assertEqual(logs, None)
    
    def test_getLogs_untouched(self):
        beforeCode = """import log4p;
                        logger.info('test1');
                        logger.info('test2');"""
        afterCode = """import log4p;
                        logger.info('test1');
                        logger.info('test2');"""
        logs = self.strat.getLogs(hash='test', filename='testFile',beforeCode=beforeCode, afterCode=afterCode, date='2023-01-01',logs=[])
        
        self.assertEqual(len(logs), 0)
        
    def test_logs_modified(self):
        beforeCode = '''import log4p;
                        logger.info("test1");
                        logger.info("test2");'''
        afterCode = '''import log4p;
                       logger.warning("test3");
                       logger.info("test2");'''
        logs = self.strat.getLogs(hash='test', filename='testFile',beforeCode=beforeCode, afterCode=afterCode, date='2023-01-01',logs=None)
        self.assertEqual(len(logs), 1)
        
    def test_logs_deleted(self):
        beforeCode = ''
        afterCode = '''import log4p;
                        logger.info("test1");
                        logger.info("test2");'''
        logs = self.strat.getLogs(hash='test', filename='testFile',beforeCode=beforeCode, afterCode=afterCode, date='2023-01-01',logs=[])

        beforeCode = '''import log4p;
                        logger.info("test1");
                        logger.info("test2");'''
        afterCode = '''import log4p;
                       logger.info("test51");'''
        logs = self.strat.getLogs(hash='test', filename='testFile',beforeCode=beforeCode, afterCode=afterCode, date='2023-01-01',logs=logs)
        self.assertEqual(len(logs), 2)
        
    
        
    def test_getLogs_deleted(self):
        beforeCode = ""
        afterCode = """import log4p;
                        logger.error("message");
                        python code ici, python code là
                        warning.info('test1');
                        logger.info('test2');"""
        logs = self.strat.getLogs(hash='test', filename='testFile',beforeCode=beforeCode, afterCode=afterCode, date='2023-01-01',logs=[])
        beforeCode = """import log4p;
                        logger.error("message");
                        python code ici, python code là
                        warning.info('test1');
                        logger.info('test2');"""
        afterCode = """import log4p;
                        logger.info('test3');"""
        logs = self.strat.getLogs(hash='test', filename='testFile',beforeCode=beforeCode, afterCode=afterCode, date='2023-01-01',logs=logs)
        
        self.assertEqual(len(logs), 3)
        
    def test_complex_logs(self):
        beforeCode = ''

        afterCode = '''import log4p;
                        logger.info("Starting processing");
                        logger.debug("Configuration loaded successfully");
                        for file in files:
                            logger.info("Processing file: %s", file);
                            logger.error("Processing file: %s", file);
                            try:
                                process_file(file);
                                logger.info("File %s processed successfully", file);
                            except Exception as e:
                                logger.error("Error while processing file %s: %s", file, e);
                        logger.info("Processing finished");'''
        logs = self.strat.getLogs(hash='test', filename='testFile',beforeCode=beforeCode, afterCode=afterCode, date='2023-01-01',logs=[])

        beforeCode = '''import log4p;
                        logger.info("Starting processing");
                        logger.debug("Configuration loaded successfully");
                        for file in files:
                            logger.info("Processing file: %s", file);
                            logger.error("Processing file: %s", file);
                            try:
                                process_file(file);
                                logger.info("File %s processed successfully", file);
                            except Exception as e:
                                logger.error("Error while processing file %s: %s", file, e);
                        logger.info("Processing finished");'''
        afterCode = '''import log4p;
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
                               logger.warning("Invalid file %s: %s", file, ve);
                       logger.info("Processing finished");'''
        logs = self.strat.getLogs(hash='test', filename='testFile',beforeCode=beforeCode, afterCode=afterCode, date='2023-01-01',logs=logs)
        self.assertEqual(len(logs), 8)
        
if __name__ == "__main__":
    unittest.main()