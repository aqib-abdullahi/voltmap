"""
Tests for VoltMap network analysis.
"""

import unittest

from generator.settings import GeneratorConfig
from generator.topology import TopologyGenerator
from generator.analysis import NetworkAnalyzer


class TestNetworkAnalyzer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        config = GeneratorConfig(random_seed=42)
        cls.network = TopologyGenerator(config).generate()
        cls.analyzer = NetworkAnalyzer(cls.network)

    def test_transformer_has_customers(self):

        transformer = self.network.network.transformers[0]
        customers = self.analyzer.customer_of_transformer(
            transformer.id
        )
        self.assertGreater(len(customers), 0)

    def test_customer_has_transformer(self):

        customer = self.network.network.customers[0]
        transformer = (
            self.analyzer.transformer_of_customer(
                customer.id
            )
        )
        self.assertIsNotNone(transformer)

    def test_feeder_has_customers(self):
        
        feeder = self.network.network.feeders[0]
        customers = self.analyzer.customer_of_feeder(
            feeder.id
        )
        self.assertGreater(len(customers), 0)
    
    def test_path_to_customer(self):
        customer = self.network.network.customers[0]
        path = self.analyzer.path_to_customer(customer.id)
        self.assertEqual(len(path), 6)
        self.assertEqual(path[-1].id, customer.id)
        self.assertEqual(path[-2].id, customer.transformer.id)

    def test_customer_connectivity(self):

        customer = self.network.network.customers[0]
        self.assertTrue(
            self.analyzer.is_customer_connected(
                customer.id
            )
        )

    def test_no_disconnected_customers(self):

        disconnected = (
            self.analyzer.disconnected_customers()
        )
        self.assertEqual(len(disconnected), 0
        )


if __name__ == "__main__":
    unittest.main()