"""
Tests for VoltMap CIM electrical topology.
"""

import unittest

from generator.settings import GeneratorConfig
from generator.topology import TopologyGenerator
from generator.cim.topology import CIMTopologyBuilder as CIMTopologyBuilder


class TestCIMTopology(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config = GeneratorConfig(random_seed=42)

        cls.network = (
            TopologyGenerator(config).generate()
        )

        cls.topology = (
            CIMTopologyBuilder(cls.network).build()
        )

    def test_connectivity_nodes_exist(self):

        self.assertGreater(
            len(self.topology.connectivity_nodes),
            0,
        )

    def test_terminals_exist(self):

        self.assertGreater(
            len(self.topology.terminals),
            0,
        )

    def test_every_terminal_has_connectivity_node(self):

        for terminal in self.topology.terminals:

            self.assertIsNotNone(
                terminal.connectivity_node
            )

    def test_every_line_has_two_terminals(self):

        line_ids = {
            line.id
            for line in self.network.line_segments
        }

        for line_id in line_ids:

            terminals = [
                terminal
                for terminal in self.topology.terminals
                if terminal.equipment_id == line_id
            ]

            self.assertEqual(
                len(terminals),
                2,
            )
        
    def test_every_switch_has_two_terminals(self):
        
        for switch in self.network.switches:

            terminals = [
                terminal
                for terminal in self.topology.terminals
                if terminal.equipment_id == switch.id
            ]

            self.assertEqual(len(terminals), 2)
    
    def test_every_feeder_has_terminal(self):

        for feeder in self.network.feeders:

            terminals = [
                terminal
                for terminal in self.topology.terminals
                if terminal.equipment_id == feeder.id
            ]

            self.assertEqual(len(terminals), 1)

    def test_every_transformer_has_two_terminals(self):

        transformer_ids = {
            transformer.id
            for transformer in self.network.transformers
        }

        for transformer_id in transformer_ids:

            terminals = [
                terminal
                for terminal in self.topology.terminals
                if terminal.equipment_id == transformer_id
            ]

            self.assertEqual(
                len(terminals),
                2,
            )

    def test_customers_are_connected(self):

        customer_ids = {
            customer.id
            for customer in self.network.customers
        }

        for customer_id in customer_ids:

            terminals = [
                terminal
                for terminal in self.topology.terminals
                if terminal.equipment_id == customer_id
            ]

            self.assertEqual(
                len(terminals),
                1,
            )

            self.assertIsNotNone(
                terminals[0].connectivity_node
            )


if __name__ == "__main__":
    unittest.main()