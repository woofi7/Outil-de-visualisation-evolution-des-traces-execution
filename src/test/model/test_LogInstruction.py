import unittest
from model.LogInstructionCollectors.LogInstruction import LogInstruction



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

if __name__ == "__main__":
    unittest.main()