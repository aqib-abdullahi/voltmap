"""
VoltMap Generator
Main entry point.
"""
import random
import config
from topology import TopologyGenerator
from validator import Validator, ValidationError
from exporter import CypherExporter
from constraints import ConstraintExporter
from statistics import Statistics
from settings import GeneratorConfig


OUTPUT_FILE = "generated_dataset.cypher"


def main():
    
    cfg = GeneratorConfig()

    print("=" * 50)
    print("VoltMap Network Generator")
    print("=" * 50)

    print("Initializing random seed...")
    random.seed(config.RANDOM_SEED)
    
    print("\nGenerating network...")
    network = TopologyGenerator(cfg).generate()

    
    print("Validating network...")
    try:
        Validator(network).validate()
    except ValidationError as error:
        print("\nValidation Failed\n")
        print(error)
        return

    print("Validation Passed ✓")

    print("Exporting Neo4j dataset...")
    exporter = CypherExporter(network)
    exporter.export(OUTPUT_FILE)
    ConstraintExporter().export("constraints.cypher")
    print("Export Complete.")

    print("\nNetwork Summary")
    print("-" * 30)

    print(f"Substations   : {len(network.substations)}")
    print(f"Feeders       : {len(network.feeders)}")
    print(f"Line Segments : {len(network.line_segments)}")
    print(f"Poles         : {len(network.poles)}")
    print(f"Switches      : {len(network.switches)}")
    print(f"Transformers  : {len(network.transformers)}")
    print(f"Customers     : {len(network.customers)}")

    print("\nOutput")
    print("-" * 30)
    print(OUTPUT_FILE)
    
    stats = Statistics(network)
    print()
    print("Network Metrics")
    print("-" * 30)

    print(f"Total line length (m): {stats.total_line_length():.2f}")
    print(f"Average line length (m): {stats.average_line_length():.2f}")
    print(
        f"Average customers/transformer: "
        f"{stats.average_customers_per_transformer():.2f}"
    )

    print("\nDone.")


if __name__ == "__main__":
    main()