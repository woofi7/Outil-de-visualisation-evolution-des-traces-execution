import unittest
from model.LogInstructionCollectors.LogInstruction import LogInstruction
from model.LogInstructionCollectors.Modification import Modification

from model.LogInstructionsFileGenerators.CsvFileGenerator import CsvFileGenerator

class test_CsvFileGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = CsvFileGenerator()

    def test_createFile(self):
        log1 = LogInstruction("level","instruction1", [], "2023-01-01")
        log2 = LogInstruction("level","instruction2", [], "2023-01-02")
        log1.add_modification(Modification("commit1", "instruction", "2023-01-01", "added", "before", "after", "hash", "filename", "author"))
        log1.add_modification(Modification("commit2", "instruction", "2023-01-04", "added", "before", "after", "hash", "filename", "author"))
        log2.add_modification(Modification("commit1", "instruction", "2023-01-02", "added", "before", "after", "hash", "filename", "author"))
        log2.add_modification(Modification("commit2", "instruction", "2023-01-05", "added", "before", "after", "hash", "filename", "author"))
        
        log_instructions = [log1, log2]

        result = self.gen.createFile(log_instructions)
        
        self.assertEqual(result, "./files/graphData.csv")
        
if __name__ == '__main__':
    unittest.main()
        