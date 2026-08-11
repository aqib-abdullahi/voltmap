
class Statistics:

    def __init__(self, topology):
        self.topology = topology

    def total_line_length(self):
        return sum(
            line.length_m
            for line in self.topology.line_segments
        )

    def average_customers_per_transformer(self):
        if not self.topology.transformers:
            return 0

        return (
            len(self.topology.customers)
            /
            len(self.topology.transformers)
        )

    def average_line_length(self):
        if not self.topology.line_segments:
            return 0

        return (
            self.total_line_length()
            /
            len(self.topology.line_segments)
        )