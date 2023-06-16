import unittest
from model.Modification import Modification


class test_Modification(unittest.TestCase):
        
    
  def test_modification(self):
     modification = Modification('commit', 'date', 'type', 'beforeCode', 'aftercode', 'hash', 'filename')
     commit = modification.get_commit_hash()
     date = modification.get_date()
     self.assertEqual(modification.get_commit_hash(), 'commit')
     self.assertEqual(modification.get_date(), 'date')

if __name__ == "__main__":
    unittest.main()