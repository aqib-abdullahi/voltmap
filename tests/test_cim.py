"""
Tests for VoltMap CIM mapping.
"""

import unittest

from generator.settings import GeneratorConfig
from generator.topology import TopologyGenerator
from generator.cim.mapping import cim_entity
from generator.cim.validator import CIMValidator


class TestCIM(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config = GeneratorConfig(random_seed=42)
        cls.network = TopologyGenerator(config).generate()

    def test_all_assets_have_cim_mapping(self):

        missing = CIMValidator().validate(
            self.network
        )
        self.assertEqual(
            missing,
            []
        )

    def test_transformer_mapping(self):

        transformer = self.network.transformers[0]
        entity = cim_entity(transformer)
        self.assertEqual(
            entity.name,
            "PowerTransformer"
        )

    def test_line_segment_mapping(self):

        line = self.network.line_segments[0]
        entity = cim_entity(line)
        self.assertEqual(
            entity.name,
            "ACLineSegment"
        )


if __name__ == "__main__":
    unittest.main()