"""
VoltMap Generator
Exports the generated network to Neo4j Cypher.
"""
from pathlib import Path
from . import config
from datetime import datetime


class CypherExporter:
    def __init__(self, topology):
        self.topology = topology
        self.lines = []

    def export(self, output_file: str):
        self.lines.clear()
        self._write_header()
        self._export_substations()
        self._export_feeders()
        self._export_line_segments()
        self._export_poles()
        self._export_switches()
        self._export_transformers()
        self._export_customers()
        self._export_relationships()
        Path(output_file).write_text(
            "\n".join(self.lines),
            encoding="utf-8"
        )

    def _add(self, line=""):
        self.lines.append(line)

    def _write_header(self):
        self._add("// VoltMap Generated Dataset")
        self._add("// Generated Automatically")
        self._add("//")
        self._add(f"//Version : {config.VERSION}")
        self._add(f"//Seed    : {config.RANDOM_SEED}")
        self._add(f"//Date    : {datetime.now().isoformat()}")
        self._add(f"//CIM    : Simplified Distribution Profile")
        self._add()

    def _export_substations(self):
        self._add("// Substations")
        
        for s in self.topology.substations:
            self._add(
                f'''MERGE (:Substation {{
                    id:"{s.id}",
                    name:"{s.name}",
                    voltage_kV:{s.voltage_kV},
                    location:"{s.location}"
                    }});'''
            )
        self._add()

    def _export_feeders(self):
        self._add("// Feeders")

        for f in self.topology.feeders:
            self._add(
                f'''MERGE (:Feeder {{
                    id:"{f.id}",
                    name:"{f.name}",
                    voltage_kV:{f.voltage_kV},
                    length_km:{f.length_km}
                    }});'''
            )
        self._add()

    def _export_line_segments(self):
        self._add("// Line Segments")
        
        for l in self.topology.line_segments:
            self._add(
                f'''MERGE (:LineSegment {{
                    id:"{l.id}",
                    name:"{l.name}",
                    voltage_kV:{l.voltage_kV},
                    length_m:{l.length_m},
                    conductor_type:"{l.conductor_type}"
                    }});'''
            )
        self._add()

    def _export_poles(self):
        self._add("// Poles")

        for p in self.topology.poles:

            self._add(
                f'''MERGE (:Pole {{
                    id:"{p.id}",
                    pole_number:"{p.pole_number}",
                    material:"{p.material}",
                    height_m:{p.height_m}
                    }});'''
            )
        self._add()

    def _export_switches(self):
        self._add("// Switches")
        
        for s in self.topology.switches:
            self._add(
                f'''MERGE (:Switch {{
                    id:"{s.id}",
                    name:"{s.name}",
                    status:"{s.status}"
                    }});'''
            )

        self._add()

    def _export_transformers(self):
        self._add("// Transformers")

        for t in self.topology.transformers:
            self._add(
                f'''MERGE (:Transformer {{
                    id:"{t.id}",
                    name:"{t.name}",
                    rating_kVA:{t.rating_kVA}
                    }});'''
            )
        self._add()

    def _export_customers(self):
        self._add("// Customers")
        
        for c in self.topology.customers:
            self._add(
                f'''MERGE (:Customer {{
                    id:"{c.id}",
                    name:"{c.name}",
                    customer_type:"{c.customer_type}",
                    load_kW:{c.load_kW}
                    }});'''
            )
        self._add()
    
    
    def _export_relationships(self):

        self._add("// Relationships")

        # Substation -> Feeder
        for feeder in self.topology.feeders:

            self._add(f"""
            MATCH (s:Substation {{id:'{feeder.source.id}'}})
            MATCH (f:Feeder {{id:'{feeder.id}'}})
            MERGE (s)-[:FEEDS]->(f);
            """)

        # Feeder -> LineSegment
        for feeder in self.topology.feeders:
            for line in feeder.line_segments:

                self._add(f"""
                MATCH (f:Feeder {{id:'{feeder.id}'}})
                MATCH (l:LineSegment {{id:'{line.id}'}})
                MERGE (f)-[:CONTAINS]->(l);
                """)

        # LineSegment -> Pole
        for line in self.topology.line_segments:
            # if line.terminal_pole:
            #     self._add(f"""
            #     MATCH (l:LineSegment {{id:'{line.id}'}})
            #     MATCH (p:Pole {{id:'{line.terminal_pole.id}'}})
            #     MERGE (l)-[:TERMINATES_AT]->(p);
            #     """)
            for pole in line.poles:
                self._add(f"""
                    MATCH (l:LineSegment {{id:'{line.id}'}})
                    MATCH (p:Pole {{id:'{pole.id}'}})
                    MERGE (l)-[:HAS_POLE]->(p);
                    """)

        # Mounted assets
        for transformer in self.topology.transformers:
            self._add(f"""
            MATCH (t:Transformer {{id:'{transformer.id}'}})
            MATCH (p:Pole {{id:'{transformer.mounted_on.id}'}})
            MERGE (t)-[:MOUNTED_ON]->(p);
            """)

        for switch in self.topology.switches:
            self._add(f"""
            MATCH (s:Switch {{id:'{switch.id}'}})
            MATCH (p:Pole {{id:'{switch.mounted_on.id}'}})
            MERGE (s)-[:MOUNTED_ON]->(p);
            """)

        # Transformer -> Customer
        for transformer in self.topology.transformers:
            for customer in transformer.customers:
                self._add(f"""
                MATCH (t:Transformer {{id:'{transformer.id}'}})
                MATCH (c:Customer {{id:'{customer.id}'}})
                MERGE (t)-[:SUPPLIES]->(c);
                """)