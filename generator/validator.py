"""
VoltMap Generator
Network validation module.
Validates structural and engineering rules before export.
"""
from collections import Counter


class ValidationError(Exception):
    """Raised when the generated network fails validation."""
    pass


class Validator:

    def __init__(self, topology):
        self.topology = topology
        self.errors = []

    def validate(self):
        """Run all validation checks."""
        self.errors.clear()
        
        self._validate_unique_ids()
        self._validate_feeders()
        self._validate_line_segments()
        self._validate_poles()
        self._validate_transformers()
        self._validate_customers()

        if self.errors:
            raise ValidationError(
                "\n".join(self.errors)
            )

        return True

    def _all_assets(self):
        return (
            self.topology.network.substations
            + self.topology.network.feeders
            + self.topology.network.line_segments
            + self.topology.network.poles
            + self.topology.network.switches
            + self.topology.network.transformers
            + self.topology.network.customers
        )

    def _validate_unique_ids(self):
        ids = [asset.id for asset in self._all_assets()]
        duplicates = [
            asset_id
            for asset_id, count in Counter(ids).items()
            if count > 1
        ]

        if duplicates:
            self.errors.append(
                f"Duplicate IDs found: {duplicates}"
            )

    def _validate_feeders(self):
        for feeder in self.topology.network.feeders:
            if feeder.source is None:
                self.errors.append(
                    f"{feeder.id} has no source substation."
                )

    # def _validate_line_segments(self):
    #     for line in self.topology.line_segments:
    #         if line.feeder is None:
    #             self.errors.append(
    #                 f"{line.id} is not assigned to a feeder."
    #             )

    #         if line.terminal_pole is None:
    #             self.errors.append(
    #                 f"{line.id} has no terminal pole."
    #             )
    def _validate_line_segments(self):
        for line in self.topology.network.line_segments:
            if line.feeder is None:
                self.errors.append(
                    f"{line.id} is not assigned to a feeder."
                )
            if len(line.poles) == 0:
                self.errors.append(
                    f"{line.id} has no poles."
                )

    def _validate_poles(self):
        """
        Validate pole properties.
        Poles are allowed to have no mounted assets.
        """
        pass
        # for pole in self.topology.poles:
        #     if len(pole.mounted_assets) == 0:
        #         self.errors.append(
        #             f"{pole.id} has no mounted assets."
        #         )

    def _validate_transformers(self):
        for transformer in self.topology.network.transformers:
            if transformer.mounted_on is None:
                self.errors.append(
                    f"{transformer.id} is not mounted on a pole."
                )

            if len(transformer.customers) == 0:
                self.errors.append(
                    f"{transformer.id} supplies no customers."
                )

    def _validate_customers(self):
        for customer in self.topology.network.customers:
            if customer.transformer is None:
                self.errors.append(
                    f"{customer.id} has no supplying transformer."
                )