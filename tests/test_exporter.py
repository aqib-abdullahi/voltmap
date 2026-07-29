"""
Tests for cypher export    
"""

import os
import unittest

from generator.topology import TopologyGenerator
from generator.exporter import CypherExporter


class TestExporter(unittest.TestCase):
    def test_export(self):
        topology = TopologyGenerator().generate()
        filename = "test.cypher"
        CypherExporter(topology).export(filename)
        self.assertTrue(os.path.exists(filename))
        os.remove(filename)
        
if __name__ == "__main__":
    unittest.main()