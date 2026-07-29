"""
Test statistics
"""

import unittest

from generator.topology import TopologyGenerator
from generator.statistics import Statistics


class TestStatistics(unittest.TestCase):
    
    def test_total_line_length(self):
        topology = TopologyGenerator().generate()
        stats = Statistics(topology)
        
        self.assertGreater(stats.total_line_length(), 0)
        
    def test_average_customer(self):
        topology = TopologyGenerator().generate()
        stats = Statistics(topology)
        self.assertGreater(stats.average_customers_per_transformer(), 0)
 

if __name__ == "__main__":
    unittest.main()