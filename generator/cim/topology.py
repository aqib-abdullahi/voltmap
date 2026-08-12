"""
VoltMap CIM Topology

Derives a CIM-oriented electrical topology from the
VoltMap synthetic network.

The VoltMap network remains unchanged.

This module introduces:
    - Terminal
    - ConnectivityNode

These represent electrical connectivity rather than
physical infrastructure.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from generator.models import (
    LineSegment,
    Switch,
    Transformer,
    Customer,
)


@dataclass
class Terminal:
    """
    Electrical connection point of a conducting equipment.
    """

    id: str
    equipment_id: str
    connectivity_node: Optional["ConnectivityNode"] = None


@dataclass
class ConnectivityNode:
    """
    Represents an electrical connectivity point.

    Multiple terminals connected to the same node are
    electrically connected.
    """

    id: str
    terminals: List[Terminal] = field(default_factory=list)


class CIMTopology:
    """
    CIM-oriented electrical topology derived from a
    VoltMap Network.
    """

    def __init__(self):
        self.connectivity_nodes = []
        self.terminals = []

    def add_node(self, node):
        self.connectivity_nodes.append(node)

    def add_terminal(self, terminal):
        self.terminals.append(terminal)

    def connect(self, terminal, node):
        terminal.connectivity_node = node
        node.terminals.append(terminal)


class CIMTopologyBuilder:
    """
    Converts a VoltMap Network into a CIM-oriented
    electrical topology.
    """

    def __init__(self, network):
        self.network = network
        self.topology = CIMTopology()

        self._node_counter = 0
        self._terminal_counter = 0

    def build(self):
        """
        Build the CIM topology from the VoltMap network.
        """

        for feeder in self.network.feeders:
            self._build_feeder(feeder)

        return self.topology

    def _new_node(self):
        self._node_counter += 1

        node = ConnectivityNode(
            id=f"CN{self._node_counter:04d}"
        )

        self.topology.add_node(node)

        return node

    def _new_terminal(self, equipment_id):
        self._terminal_counter += 1

        terminal = Terminal(
            id=f"T{self._terminal_counter:04d}",
            equipment_id=equipment_id,
        )

        self.topology.add_terminal(terminal)

        return terminal

    def _build_feeder(self, feeder):
        """
        Build the electrical path of one feeder.

        Consecutive line segments share a connectivity node.
        """

        previous_node = self._new_node()
        
        self._connect_feeder(
            feeder,
            previous_node
        )

        for line in feeder.line_segments:

            next_node = self._new_node()

            self._connect_line(
                line,
                previous_node,
                next_node,
            )

            # Assets mounted on the pole associated with
            # this line segment are connected to the
            # downstream electrical node.
            for pole in line.poles:
                for asset in pole.mounted_assets:

                    if isinstance(asset, Switch):
                        self._connect_switch(
                            asset,
                            previous_node,
                            next_node,
                        )

                    elif isinstance(asset, Transformer):
                        self._connect_transformer(
                            asset,
                            next_node,
                        )

            previous_node = next_node
    
    def _connect_feeder(
        self,
        feeder,
        node: ConnectivityNode,
    ):
        """
        Connect the feeder to its source-side connectivity node.
        """

        terminal = self._new_terminal(feeder.id)

        self.topology.connect(
            terminal,
            node,
        )

    def _connect_line(
        self,
        line: LineSegment,
        from_node: ConnectivityNode,
        to_node: ConnectivityNode,
    ):
        """
        An ACLineSegment has two electrical terminals.
        """

        from_terminal = self._new_terminal(line.id)
        to_terminal = self._new_terminal(line.id)

        self.topology.connect(
            from_terminal,
            from_node,
        )

        self.topology.connect(
            to_terminal,
            to_node,
        )

    # def _connect_switch(
    #     self,
    #     switch: Switch,
    #     node: ConnectivityNode,
    # ):
    #     """
    #     Connect a switch to the electrical node on which
    #     it is mounted.
    #     """

    #     terminal = self._new_terminal(switch.id)

    #     self.topology.connect(
    #         terminal,
    #         node,
    #     )
    def _connect_switch(
        self,
        switch: Switch,
        from_node: ConnectivityNode,
        to_node: ConnectivityNode,
    ):
        """
        Connect a switch between two electrical connectivity nodes.

        A switch is a conducting equipment with two terminals.
        """

        from_terminal = self._new_terminal(switch.id)
        to_terminal = self._new_terminal(switch.id)

        self.topology.connect(
            from_terminal,
            from_node,
        )

        self.topology.connect(
            to_terminal,
            to_node,
        )

    def _connect_transformer(
        self,
        transformer: Transformer,
        primary_node: ConnectivityNode,
    ):
        """
        Create primary and secondary terminals for a
        distribution transformer.

        The secondary side receives a separate connectivity
        node because it represents a different voltage level.
        """

        primary_terminal = self._new_terminal(
            transformer.id
        )

        self.topology.connect(
            primary_terminal,
            primary_node,
        )

        secondary_node = self._new_node()

        secondary_terminal = self._new_terminal(
            transformer.id
        )

        self.topology.connect(
            secondary_terminal,
            secondary_node,
        )

        for customer in transformer.customers:
            self._connect_customer(
                customer,
                secondary_node,
            )

    def _connect_customer(
        self,
        customer: Customer,
        node: ConnectivityNode,
    ):
        """
        Connect an EnergyConsumer to the transformer
        secondary network.

        This is an intentional synthetic abstraction:
        the current VoltMap model does not generate
        individual service lines.
        """

        terminal = self._new_terminal(
            customer.id
        )

        self.topology.connect(
            terminal,
            node,
        )
        