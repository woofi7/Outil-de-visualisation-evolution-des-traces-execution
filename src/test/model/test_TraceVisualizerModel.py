import unittest
from model.TraceVisualizerModel import TraceVisualizerModel
from model.Modification import Modification
from unittest.mock import Mock
from git import Repo



class test_TraceVizualizerModel(unittest.TestCase):
        
    
  def test_getCommitChanges(self):
    tvm = TraceVisualizerModel()
    modification = Modification('commit', 'date', 'type', 'beforeCode', 'aftercode', 'hash', 'filename')
    tvm.getCommitChanges([modification])


if __name__ == "__main__":
    unittest.main()