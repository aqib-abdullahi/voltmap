"""
Test for network validation   
"""

import unittest

from generator.topology import TopologyGenerator
from generator.validator import Validator


class TestValidator(unittest.TestCase):
    
    def test_valid_network(self):
        topology = TopologyGenerator().generate()
        validator = Validator(topology)
        self.assertTrue(validator.validate())


if __name__ == "__main__":
    unittest.main()