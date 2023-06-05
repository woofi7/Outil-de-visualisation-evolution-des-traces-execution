import unittest
from model.LogInstruction import LogInstruction



class test_LogInstruction(unittest.TestCase):
        
    
  def test_add_modification(self):
     logInstruction = LogInstruction('log.info("info")', [])
     logInstruction.add_modification('log.trace("info")')
     self.assertEqual(logInstruction.instruction, 'log.info("info")')
     self.assertEqual(len(logInstruction.modifications), 1)
     self.assertEqual(logInstruction.modifications[0], 'log.trace("info")')

  def test_addModification_none_mod(self):
     logInstruction = LogInstruction('log.info("info")', None)
     self.assertEqual(logInstruction.instruction, 'log.info("info")')
     self.assertIsNotNone(logInstruction.modifications)

if __name__ == "__main__":
    unittest.main()