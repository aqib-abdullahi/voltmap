"""
test topology generatio
"""

import unittest
from generator.topology import TopologyGenerator

class TestTopology(unittest.TestCase):
    
    def test_generation(self):
        
        topology = TopologyGenerator().generate()        
        self.assertGreater(len(topology.substations), 0)
        self.assertGreater(len(topology.feeders), 0)
        self.assertGreater(len(topology.line_segments), 0)
        self.assertGreater(len(topology.poles), 0)
        self.assertGreater(len(topology.transformers), 0)
        self.assertGreater(len(topology.customers), 0)

    def test_every_feeder_has_source(self):
        topology = TopologyGenerator().generate()
        for feeder in topology.feeders:
            self.assertIsNotNone(feeder.source)

    def test_every_line_has_poles(self):
        topology = TopologyGenerator().generate()
        for line in topology.line_segments:
            self.assertGreater(len(line.poles), 0)

if __name__ == "__main__":
    unittest.main()