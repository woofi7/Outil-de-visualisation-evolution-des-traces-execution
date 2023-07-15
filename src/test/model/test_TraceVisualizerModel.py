import unittest
from model.LogInstructionDiffGenerator import LogInstructionDiffGenerator
from model.LogInstructionCollectors.Modification import Modification
from unittest.mock import Mock, patch
from git import Repo



class test_TraceVizualizerModel(unittest.TestCase):
        
    
  def test_getCommitChanges(self):
    tvm = LogInstructionDiffGenerator()
    modification = Modification('commit','instruction', 'date', 'type', 'beforeCode', 'aftercode', 'hash', 'filename')
    tvm.getCommitChanges([modification])



if __name__ == "__main__":
    unittest.main()