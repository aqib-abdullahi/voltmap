# """
# VoltMap Generator
# Main entry point.
# """
# import random
# import config
# from topology import TopologyGenerator
# from validator import Validator, ValidationError
# from exporter import CypherExporter
# from constraints import ConstraintExporter
# from statistics import Statistics
# from settings import GeneratorConfig


# OUTPUT_FILE = "generated_dataset.cypher"


# def main():
    
#     cfg = GeneratorConfig()

#     print("=" * 50)
#     print("VoltMap Network Generator")
#     print("=" * 50)

#     print("Initializing random seed...")
#     random.seed(config.RANDOM_SEED)
    
#     print("\nGenerating network...")
#     network = TopologyGenerator(cfg).generate()

    
#     print("Validating network...")
#     try:
#         Validator(network).validate()
#     except ValidationError as error:
#         print("\nValidation Failed\n")
#         print(error)
#         return

#     print("Validation Passed ✓")

#     print("Exporting Neo4j dataset...")
#     exporter = CypherExporter(network)
#     exporter.export(OUTPUT_FILE)
#     ConstraintExporter().export("constraints.cypher")
#     print("Export Complete.")

#     print("\nNetwork Summary")
#     print("-" * 30)

#     print(f"Substations   : {len(network.substations)}")
#     print(f"Feeders       : {len(network.feeders)}")
#     print(f"Line Segments : {len(network.line_segments)}")
#     print(f"Poles         : {len(network.poles)}")
#     print(f"Switches      : {len(network.switches)}")
#     print(f"Transformers  : {len(network.transformers)}")
#     print(f"Customers     : {len(network.customers)}")

#     print("\nOutput")
#     print("-" * 30)
#     print(OUTPUT_FILE)
    
#     stats = Statistics(network)
#     print()
#     print("Network Metrics")
#     print("-" * 30)

#     print(f"Total line length (m): {stats.total_line_length():.2f}")
#     print(f"Average line length (m): {stats.average_line_length():.2f}")
#     print(
#         f"Average customers/transformer: "
#         f"{stats.average_customers_per_transformer():.2f}"
#     )

#     print("\nDone.")


# if __name__ == "__main__":
#     main()


"""
VoltMap Network Generator

Main entry point for generating a synthetic power
distribution network and its CIM-oriented representation.
"""

from pathlib import Path

from generator.settings import GeneratorConfig
from generator.topology import TopologyGenerator
from generator.validator import Validator
from generator.exporter import CypherExporter

from generator.cim.validator import CIMValidator
from generator.cim.topology import CIMTopologyBuilder
from generator.cim.exporter import CIMCypherExporter


def main():
    print("=" * 50)
    print("VoltMap Network Generator")
    print("=" * 50)

    # Generate VoltMap network
    print("\nGenerating network...")

    config = GeneratorConfig(random_seed=42)

    network = TopologyGenerator(config).generate()

    # Validate VoltMap network
    print("Validating VoltMap network...")

    Validator(network).validate()

    print("VoltMap validation passed ✓")

    # Validate CIM mappings
    print("Validating CIM mappings...")

    missing_mappings = CIMValidator().validate(network)

    if missing_mappings:
        print("CIM validation failed")

        for asset in missing_mappings:
            print(f"No CIM mapping for {asset.id}")

        return

    print("CIM mapping validation passed ✓")

    # Build CIM electrical topology
    print("Building CIM topology...")

    cim_topology = CIMTopologyBuilder(network).build()

    print("CIM topology built ✓")

    # Export standard VoltMap graph
    voltmap_output = Path("generated_dataset.cypher")

    print("\nExporting VoltMap Neo4j dataset...")

    CypherExporter(network).export(voltmap_output)

    print("VoltMap export complete ✓")

    # Export CIM-oriented graph
    cim_output = Path("generated_cim_dataset.cypher")

    print("Exporting CIM-oriented Neo4j dataset...")

    CIMCypherExporter(network).export(cim_output)

    print("CIM export complete ✓")

    # Summary
    print("\nNetwork Summary")
    print("-" * 30)

    print(
        f"Substations        : "
        f"{len(network.substations)}"
    )

    print(
        f"Feeders            : "
        f"{len(network.feeders)}"
    )

    print(
        f"Line Segments      : "
        f"{len(network.line_segments)}"
    )

    print(
        f"Poles              : "
        f"{len(network.poles)}"
    )

    print(
        f"Switches           : "
        f"{len(network.switches)}"
    )

    print(
        f"Transformers       : "
        f"{len(network.transformers)}"
    )

    print(
        f"Customers          : "
        f"{len(network.customers)}"
    )

    print("\nCIM Topology Summary")
    print("-" * 30)

    print(
        f"Connectivity Nodes : "
        f"{len(cim_topology.connectivity_nodes)}"
    )

    print(
        f"Terminals          : "
        f"{len(cim_topology.terminals)}"
    )

    print("\nOutput")
    print("-" * 30)

    print(voltmap_output)
    print(cim_output)

    print("\nDone.")


if __name__ == "__main__":
    main()