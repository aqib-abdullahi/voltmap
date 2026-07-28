"""
Tests for id generation
"""

import unittest
from generator.ids import IDGenerator


class TestIDGenerator(unittest.TestCase):
    
    def test_increment(self):
        ids = IDGenerator()
        self.assertEqual(ids.next("SS"), "SS001")
        self.assertEqual(ids.next("SS"), "SS002")
        self.assertEqual(ids.next("SS"), "SS003")
    
    def test_custom_width(self):
        ids = IDGenerator()
        self.assertEqual(ids.next("C", width=4), "C0001")

if __name__ == "__main__":
    unittest.main()