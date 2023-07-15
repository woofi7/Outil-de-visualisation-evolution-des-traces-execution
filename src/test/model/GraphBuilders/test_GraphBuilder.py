import unittest
from model.GraphBuilders.GraphBuilder import GraphBuilder

class test_GraphBuilder(unittest.TestCase):
    def setUp(self):
        self.gen = GraphBuilder()