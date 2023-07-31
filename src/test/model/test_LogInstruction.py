import unittest
from model.LogInstructionCollectors.LogInstruction import LogInstruction
from model.LogInstructionCollectors.Modification import Modification




class test_LogInstruction(unittest.TestCase):
        
    
  def test_add_modification(self):
     logInstruction = LogInstruction('info','"info"', [], '2023-01-01')
     logInstruction.add_modification('log.trace("info")')
     self.assertEqual(logInstruction.instruction, '"info"')
     self.assertEqual(len(logInstruction.modifications), 1)
     self.assertEqual(logInstruction.modifications[0], 'log.trace("info")')

  def test_addModification_none_mod(self):
     logInstruction = LogInstruction('info','"info"', None, '2023-01-01')
     self.assertEqual(logInstruction.instruction, '"info"')
     self.assertIsNotNone(logInstruction.modifications)

  def test_copy(self):
     modification = Modification('commit','instruction', 'date', 'type', 'beforeCode', 'aftercode', 'hash', 'filename', 'author')
     logInstruction = LogInstruction('info','"info"', [modification], '2023-01-01')
     logInstruction1 = LogInstruction.copy(logInstruction)
     self.assertEqual(logInstruction1.instruction, '"info"')
     self.assertEqual(len(logInstruction1.modifications), 1)
     self.assertEqual(logInstruction1.modifications[0].level, modification.level)

if __name__ == "__main__":
    unittest.main()