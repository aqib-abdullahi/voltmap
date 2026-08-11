"""
test topology generatio
"""

import unittest
from generator.topology import TopologyGenerator

class TestTopology(unittest.TestCase):
    
    def test_generation(self):
        
        topology = TopologyGenerator().generate()        
        self.assertGreater(len(topology.network.substations), 0)
        self.assertGreater(len(topology.network.feeders), 0)
        self.assertGreater(len(topology.network.line_segments), 0)
        self.assertGreater(len(topology.network.poles), 0)
        self.assertGreater(len(topology.network.transformers), 0)
        self.assertGreater(len(topology.network.customers), 0)

    def test_every_feeder_has_source(self):
        topology = TopologyGenerator().generate()
        for feeder in topology.network.feeders:
            self.assertIsNotNone(feeder.source)

    def test_every_line_has_poles(self):
        topology = TopologyGenerator().generate()
        for line in topology.network.line_segments:
            self.assertGreater(len(line.poles), 0)

if __name__ == "__main__":
    unittest.main()