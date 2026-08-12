"""
VoltMap CIM Graph Exporter.

Exports a VoltMap Network and its derived CIM-oriented
electrical topology to Neo4j Cypher.
"""

from pathlib import Path

from .mapping import cim_name
from .topology import CIMTopologyBuilder


class CIMCypherExporter:
    """
    Export a VoltMap network as a CIM-oriented Neo4j graph.
    """

    def __init__(self, network):
        self.network = network
        self.topology = CIMTopologyBuilder(
            network
        ).build()

        self.lines = []

    def export(self, output_file: str):
        """
        Export the CIM-oriented graph to a Cypher file.
        """

        self.lines.clear()

        self._write_header()

        # CIM equipment
        self._export_equipment()

        # CIM topology objects
        self._export_connectivity_nodes()
        self._export_terminals()

        # Relationships
        self._export_asset_relationships()
        self._export_terminal_relationships()
        self._export_connectivity_relationships()

        Path(output_file).write_text(
            "\n".join(self.lines),
            encoding="utf-8"
        )

    def _add(self, line=""):
        self.lines.append(line)

    def _write_header(self):
        self._add("// VoltMap CIM-Oriented Dataset")
        self._add("// Generated Automatically")
        self._add()

    # Equipment Export
    def _asset_collections(self):
        """
        Return all VoltMap asset collections.
        """

        return (
            self.network.substations,
            self.network.feeders,
            self.network.line_segments,
            self.network.poles,
            self.network.switches,
            self.network.transformers,
            self.network.customers,
        )

    def _export_equipment(self):
        """
        Export VoltMap assets using their CIM class names
        as Neo4j labels.
        """

        self._add("// CIM Equipment")

        for collection in self._asset_collections():

            for asset in collection:

                label = cim_name(asset)

                properties = self._asset_properties(asset)

                self._add(
                    f"MERGE (:{label} {{"
                    f"{properties}"
                    f"}});"
                )

        self._add()

    def _asset_properties(self, asset):
        """
        Build the Cypher property string for an asset.

        Every asset has an id and name. Additional properties
        are added when available.
        """

        properties = [
            f'id: "{asset.id}"',
            f'name: "{asset.name}"',
        ]

        # Substation / Feeder / Line
        if hasattr(asset, "voltage_kV"):
            properties.append(
                f"voltage_kV: {asset.voltage_kV}"
            )

        # Substation
        if hasattr(asset, "location"):
            properties.append(
                f'location: "{asset.location}"'
            )

        # Feeder
        if hasattr(asset, "length_km"):
            properties.append(
                f"length_km: {asset.length_km}"
            )

        # LineSegment
        if hasattr(asset, "length_m"):
            properties.append(
                f"length_m: {asset.length_m}"
            )

        if hasattr(asset, "conductor_type"):
            properties.append(
                f'conductor_type: '
                f'"{asset.conductor_type}"'
            )

        if hasattr(asset, "conductor_size_mm2"):
            properties.append(
                f"conductor_size_mm2: "
                f"{asset.conductor_size_mm2}"
            )

        # Pole
        if hasattr(asset, "pole_number"):
            properties.append(
                f'pole_number: "{asset.pole_number}"'
            )

        if hasattr(asset, "material"):
            properties.append(
                f'material: "{asset.material}"'
            )

        if hasattr(asset, "height_m"):
            properties.append(
                f"height_m: {asset.height_m}"
            )

        # Switch
        if hasattr(asset, "switch_type"):
            properties.append(
                f'switch_type: "{asset.switch_type}"'
            )

        if hasattr(asset, "status"):
            properties.append(
                f'status: "{asset.status}"'
            )

        if hasattr(asset, "normally_closed"):
            properties.append(
                f"normally_closed: "
                f"{str(asset.normally_closed).lower()}"
            )

        # Transformer
        if hasattr(asset, "rating_kVA"):
            properties.append(
                f"rating_kVA: {asset.rating_kVA}"
            )

        if hasattr(asset, "primary_voltage"):
            properties.append(
                f"primary_voltage: "
                f"{asset.primary_voltage}"
            )

        if hasattr(asset, "secondary_voltage"):
            properties.append(
                f"secondary_voltage: "
                f"{asset.secondary_voltage}"
            )

        if hasattr(asset, "vector_group"):
            properties.append(
                f'vector_group: "{asset.vector_group}"'
            )

        if hasattr(asset, "cooling"):
            properties.append(
                f'cooling: "{asset.cooling}"'
            )

        # Customer
        if hasattr(asset, "customer_type"):
            properties.append(
                f'customer_type: '
                f'"{asset.customer_type}"'
            )

        if hasattr(asset, "load_kW"):
            properties.append(
                f"load_kW: {asset.load_kW}"
            )

        return ", ".join(properties)

    # CIM Topology Export
    def _export_connectivity_nodes(self):
        """
        Export CIM ConnectivityNodes.
        """

        self._add("// Connectivity Nodes")

        for node in self.topology.connectivity_nodes:

            self._add(
                f'MERGE (:ConnectivityNode {{'
                f'id: "{node.id}"'
                f'}});'
            )

        self._add()

    def _export_terminals(self):
        """
        Export CIM Terminals.
        """

        self._add("// Terminals")

        for terminal in self.topology.terminals:

            self._add(
                f'MERGE (:Terminal {{'
                f'id: "{terminal.id}", '
                f'equipment_id: "{terminal.equipment_id}"'
                f'}});'
            )

        self._add()

    # Asset Relationships
    def _export_asset_relationships(self):
        """
        Export structural relationships from the
        original VoltMap network.
        """

        self._add("// Asset Relationships")

        # Substation -> Feeder
        for feeder in self.network.feeders:

            if feeder.source is not None:

                self._add(f"""
                    MATCH (s:Substation {{id: "{feeder.source.id}"}})
                    MATCH (f:Feeder {{id: "{feeder.id}"}})
                    MERGE (s)-[:FEEDS]->(f);
                    """)

        # Feeder -> ACLineSegment
        for feeder in self.network.feeders:

            for line in feeder.line_segments:

                self._add(f"""
                    MATCH (f:Feeder {{id: "{feeder.id}"}})
                    MATCH (l:ACLineSegment {{id: "{line.id}"}})
                    MERGE (f)-[:CONTAINS]->(l);
                    """)

        # ACLineSegment -> Pole
        for line in self.network.line_segments:

            for pole in line.poles:

                self._add(f"""
                    MATCH (l:ACLineSegment {{id: "{line.id}"}})
                    MATCH (p:Pole {{id: "{pole.id}"}})
                    MERGE (l)-[:HAS_POLE]->(p);
                    """)

        # Switch -> Pole
        for switch in self.network.switches:

            if switch.mounted_on is not None:

                self._add(f"""
                    MATCH (s:Switch {{id: "{switch.id}"}})
                    MATCH (p:Pole {{id: "{switch.mounted_on.id}"}})
                    MERGE (s)-[:MOUNTED_ON]->(p);
                    """)

        # Transformer -> Pole
        for transformer in self.network.transformers:

            if transformer.mounted_on is not None:

                self._add(f"""
                    MATCH (t:PowerTransformer {{id: "{transformer.id}"}})
                    MATCH (p:Pole {{id: "{transformer.mounted_on.id}"}})
                    MERGE (t)-[:MOUNTED_ON]->(p);
                    """)

        # Transformer -> Customer
        for transformer in self.network.transformers:

            for customer in transformer.customers:

                self._add(f"""
                    MATCH (t:PowerTransformer {{id: "{transformer.id}"}})
                    MATCH (c:EnergyConsumer {{id: "{customer.id}"}})
                    MERGE (t)-[:SUPPLIES]->(c);
                    """)

        self._add()

    # Terminal Relationships
    def _export_terminal_relationships(self):
        """
        Connect each CIM equipment object to its terminals.
        """

        self._add("// Equipment -> Terminal")

        for terminal in self.topology.terminals:

            asset = self._find_asset(
                terminal.equipment_id
            )

            if asset is None:
                continue

            label = cim_name(asset)

            self._add(f"""
                MATCH (e:{label} {{
                    id: "{terminal.equipment_id}"
                }})
                MATCH (t:Terminal {{
                    id: "{terminal.id}"
                }})
                MERGE (e)-[:HAS_TERMINAL]->(t);
                """)

        self._add()

    # Electrical Connectivity
    def _export_connectivity_relationships(self):
        """
        Connect terminals to ConnectivityNodes.
        """

        self._add("// Terminal -> ConnectivityNode")

        for terminal in self.topology.terminals:

            node = terminal.connectivity_node

            if node is None:
                continue

            self._add(f"""
                MATCH (t:Terminal {{
                    id: "{terminal.id}"
                }})
                MATCH (cn:ConnectivityNode {{
                    id: "{node.id}"
                }})
                MERGE (t)-[:CONNECTED_TO]->(cn);
                """)

        self._add()

    # Asset Lookup
    def _find_asset(self, asset_id):
        """
        Find an asset in the VoltMap network by ID.

        This allows a Terminal to determine which CIM
        equipment node it belongs to.
        """

        for collection in self._asset_collections():

            for asset in collection:

                if asset.id == asset_id:
                    return asset

        return None