import unittest
from model.LogInstructionCollectors.LogInstruction import LogInstruction
from model.LogInstructionCollectors.Modification import Modification

from model.LogInstructionsFileGenerators.CsvFileGenerator import CsvFileGenerator

class test_CsvFileGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = CsvFileGenerator()

    def test_createFile(self):
        log1 = LogInstruction("instruction1", None, "2023-01-01")
        log2 = LogInstruction("instruction2", None, "2023-01-02")
        log1.add_modification(Modification("commit1", "2023-01-01", "added", "before", "after", "hash", "filename"))
        log1.add_modification(Modification("commit2", "2023-01-04", "added", "before", "after", "hash", "filename"))
        log2.add_modification(Modification("commit1", "2023-01-02", "added", "before", "after", "hash", "filename"))
        log2.add_modification(Modification("commit2", "2023-01-05", "added", "before", "after", "hash", "filename"))
        
        logInstructions = [log1, log2]

        result = self.gen.createFile(logInstructions)
        
        self.assertEqual(result, "csv/data.csv")
        
if __name__ == '__main__':
    unittest.main()
        