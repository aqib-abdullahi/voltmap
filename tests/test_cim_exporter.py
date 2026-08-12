"""
Tests for the VoltMap CIM Cypher exporter.
"""

import os
import unittest

from generator.settings import GeneratorConfig
from generator.topology import TopologyGenerator
from generator.cim.exporter import CIMCypherExporter


class TestCIMCypherExporter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config = GeneratorConfig(
            random_seed=42
        )

        cls.network = (
            TopologyGenerator(config).generate()
        )

        cls.filename = "test_cim_dataset.cypher"

        exporter = CIMCypherExporter(
            cls.network
        )

        exporter.export(cls.filename)

        with open(
            cls.filename,
            "r",
            encoding="utf-8"
        ) as file:
            cls.content = file.read()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.filename):
            os.remove(cls.filename)

    def test_file_is_created(self):
        self.assertTrue(
            os.path.exists(self.filename)
        )

    def test_cim_equipment_is_exported(self):
        self.assertIn(
            ":Substation",
            self.content
        )

        self.assertIn(
            ":Feeder",
            self.content
        )

        self.assertIn(
            ":ACLineSegment",
            self.content
        )

        self.assertIn(
            ":PowerTransformer",
            self.content
        )

        self.assertIn(
            ":EnergyConsumer",
            self.content
        )

    def test_connectivity_nodes_are_exported(self):
        self.assertIn(
            ":ConnectivityNode",
            self.content
        )

    def test_terminals_are_exported(self):
        self.assertIn(
            ":Terminal",
            self.content
        )

    def test_equipment_terminal_relationship_exists(self):
        self.assertIn(
            "[:HAS_TERMINAL]",
            self.content
        )

    def test_terminal_connectivity_relationship_exists(self):
        self.assertIn(
            "[:CONNECTED_TO]",
            self.content
        )


if __name__ == "__main__":
    unittest.main()