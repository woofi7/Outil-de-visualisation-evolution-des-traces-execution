import unittest
from model.Modification import Modification


class test_Modification(unittest.TestCase):
        
    
  def test_modification(self):
     modification = Modification('commit', 'date', 'type')
     commit = modification.get_commit_hash()
     date = modification.get_date()
     self.assertEqual(commit, 'commit')
     self.assertEqual(date, 'date')

if __name__ == "__main__":
    unittest.main()