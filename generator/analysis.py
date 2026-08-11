"""
Voltmap Network Analysis

Graph Oriented analysis operations over an in-memory
distribution network.
"""

from collections import deque

from .models import Transformer



class NetworkAnalyzer:
    
    def __init__(self, network):
        self.network = network
    
    # Basic topology queries
    def customer_of_transformer(self, transformer_id):
        """
        Returns a list of customers connected to the given transformer.
        """
        # return [
        #     customer
        #     for customer in self.network.customers
        #     if customer.transformer_id == transformer_id
        # ]

        for transformer in self.network.transformers:
            if transformer.id == transformer_id:
                return list(transformer.customers)
        return []
    
    def transformer_of_customer(self, customer_id):
        """
        Returns the transformer connected to the given customer.
        """
        for customer in self.network.customers:
            if customer.id == customer_id:
                return customer.transformer
        return None
    
    def feeders_of_substation(self, substation_id):
        """
        Returns a list of feeders originating from the given substation.
        """
        for substation in self.network.substations:
            if substation.id == substation_id:
                return list(substation.feeders)
        return []

    def customer_of_feeder(self, feeder_id):
        """
        Return all customers supplied downstream
        of a feeder.
        """
        feeder = None
        for candidate in self.network.feeders:
            if candidate.id == feeder_id:
                feeder = candidate
                break

        if feeder is None:
            return []

        customers = []

        for line in feeder.line_segments:
            for pole in line.poles:
                for asset in pole.mounted_assets:
                    if isinstance(asset, Transformer):
                        customers.extend(asset.customers)

        return customers
    
    def total_load_of_feeder(self, feeder_id):
        """
        Returns the total load of all customers downstream of a feeder.
        """
        customers = self.customer_of_feeder(feeder_id)
        return sum(customer.load_kw for customer in customers)
    
    # Path tracing
    def path_to_customer(self, customer_id):
        """
        Return the asset path from the customer's substation
        to the customer.

        Example:

        Substation
          -> Feeder
          -> LineSegment
          -> Pole
          -> Transformer
          -> Customer
        """

        customer = None
        for candidate in self.network.customers:

            if candidate.id == customer_id:
                customer = candidate
                break

        if customer is None:
            return []

        transformer = customer.transformer

        if transformer is None:
            return []

        pole = transformer.mounted_on

        if pole is None:
            return []

        line = self._line_containing_pole(pole)

        if line is None:
            return []

        feeder = line.feeder

        if feeder is None:
            return []

        substation = feeder.source

        if substation is None:
            return []

        return [
            substation,
            feeder,
            line,
            pole,
            transformer,
            customer,
        ]
    
    def _line_containing_pole(self, pole):
        """
        Returns the line segment containing the given pole.
        """
        for line in self.network.line_segments:
            if pole in line.poles:
                return line
        return None
    
    # Transformer Service Area
    def transformer_service_area(self, transformer_id):
        """ 
        Return customers served by a transformer and their aggregate load.
        """
        
        customers = self.customer_of_transformer(transformer_id)
        total_load = sum(customer.load_kw for customer in customers)
        
        return {
            "transformer_id": transformer_id,
            "customer_count": len(customers),
            "total_load_kw": total_load,
            "customers": customers,
        }
        
    # Connectivity
    def is_customer_connected(self, customer_id):
        """
        Determine whether a customer has a complete topological connection
        to a substation
        """
        path = self.path_to_customer(customer_id)
        return len(path) == 6
    
    # Network wide analysis
    def disconnected_customers(self):
        """
        Returns a list of customers that are not connected to a substation.
        """
        disconnected = []
        for customer in self.network.customers:
            if not self.is_customer_connected(customer.id):
                disconnected.append(customer)
        
        return disconnected
    