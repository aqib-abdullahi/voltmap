"""
Validate that every VoltMap asset has a CIM mapping.
"""
from .mapping import MODEL_TO_CIM


class CIMValidator:

    def validate(self, network):
        missing = []

        for collection in (
            network.substations,
            network.feeders,
            network.line_segments,
            network.poles,
            network.switches,
            network.transformers,
            network.customers,
        ):

            for asset in collection:
                if type(asset) not in MODEL_TO_CIM:
                    missing.append(asset)
        return missing