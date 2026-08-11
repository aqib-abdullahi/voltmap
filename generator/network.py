"""
VoltMap Network.
Represents a complete synthetic distribution network.
"""

from dataclasses import dataclass, field

from .models import (
    Substation,
    Feeder,
    LineSegment,
    Pole,
    Switch,
    Transformer,
    Customer,
)


@dataclass
class Network:

    substations: list[Substation] = field(default_factory=list)
    feeders: list[Feeder] = field(default_factory=list)
    line_segments: list[LineSegment] = field(default_factory=list)
    poles: list[Pole] = field(default_factory=list)
    switches: list[Switch] = field(default_factory=list)
    transformers: list[Transformer] = field(default_factory=list)
    customers: list[Customer] = field(default_factory=list)