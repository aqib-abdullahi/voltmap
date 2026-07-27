"""
Neo4j constraint exporter.
"""

from pathlib import Path


class ConstraintExporter:
    CONSTRAINTS = [

        "Substation",
        "Feeder",
        "LineSegment",
        "Pole",
        "Switch",
        "Transformer",
        "Customer",

    ]

    def export(self, filename):
        lines = []

        lines.append("// VoltMap Constraints")
        lines.append("")
        for label in self.CONSTRAINTS:
            lines.append(
                f"""CREATE CONSTRAINT {label.lower()}_id
                IF NOT EXISTS
                FOR (n:{label})
                REQUIRE n.id IS UNIQUE;
                """
            )

        Path(filename).write_text(
            "\n".join(lines),
            encoding="utf-8"
        )