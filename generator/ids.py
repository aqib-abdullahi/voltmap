"""
VoltMap Generator
Unique ID generation utilities.
"""
from collections import defaultdict


class IDGenerator:
    """
    Generates sequential IDs for every asset type.
    Example:
        SS001
        SS002
        F001
        F002
        LS001
        P001
        TR001
        C0001
    """

    def __init__(self):
        self._counters = defaultdict(int)

    def next(self, prefix: str, width: int = 3) -> str:
        """
        Generate the next identifier.

        Parameters:
        prefix : str
            Asset prefix (SS, F, LS, P, TR, C)

        width : int
            Number of digits

        Returns:
        str
            Generated identifier.
        """

        self._counters[prefix] += 1
        number = self._counters[prefix]
        return f"{prefix}{number:0{width}d}"

    def reset(self):
        """Reset all counters."""
        self._counters.clear()