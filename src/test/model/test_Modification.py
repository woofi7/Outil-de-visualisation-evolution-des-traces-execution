import unittest
from model.LogInstructionCollectors.Modification import Modification


class test_Modification(unittest.TestCase):
        
    
  def test_modification(self):
     modification = Modification('commit','instruction', 'date', 'type', 'beforeCode', 'aftercode', 'hash', 'filename')
     commit = modification.get_commit_hash()
     date = modification.get_date()
     self.assertEqual(modification.get_commit_hash(), 'hash')
     self.assertEqual(modification.get_date(), 'date')

if __name__ == "__main__":
    unittest.main()