"""
VoltMap Generator
Main entry point.
"""
from topology import TopologyGenerator
from validator import Validator, ValidationError
from exporter import CypherExporter


OUTPUT_FILE = "generated_dataset.cypher"


def main():

    print("=" * 50)
    print("VoltMap Network Generator")
    print("=" * 50)

    
    print("\nGenerating network...")
    topology = TopologyGenerator().generate()

    
    print("Validating network...")
    try:
        Validator(topology).validate()
    except ValidationError as error:
        print("\nValidation Failed\n")
        print(error)
        return

    print("Validation Passed ✓")

    print("Exporting Neo4j dataset...")
    exporter = CypherExporter(topology)
    exporter.export(OUTPUT_FILE)
    print("Export Complete ✓")

    print("\nNetwork Summary")
    print("-" * 30)

    print(f"Substations   : {len(topology.substations)}")
    print(f"Feeders       : {len(topology.feeders)}")
    print(f"Line Segments : {len(topology.line_segments)}")
    print(f"Poles         : {len(topology.poles)}")
    print(f"Switches      : {len(topology.switches)}")
    print(f"Transformers  : {len(topology.transformers)}")
    print(f"Customers     : {len(topology.customers)}")

    print("\nOutput")
    print("-" * 30)
    print(OUTPUT_FILE)

    print("\nDone.")


if __name__ == "__main__":
    main()