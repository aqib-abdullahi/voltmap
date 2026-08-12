"""
VoltMap Generator
Core data models for representing electrical distribution
network assets.
"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Asset:
    """Base class for all VoltMap assets."""

    id: str
    name: str


@dataclass
class Substation(Asset):
    voltage_kV: float
    location: str
    feeders: List["Feeder"] = field(default_factory=list)


@dataclass
class Feeder(Asset):
    voltage_kV: float
    # length_km: lambda self: sum(line.length_m for line in self.line_segments) / 1000
    source: Optional[Substation] = None
    line_segments: List["LineSegment"] = field(default_factory=list)
    
    @property
    def length_km(self):
        """
        Total feeder length in kilometres.
        """
        total_length_m = sum(
            line.length_m
            for line in self.line_segments
        )

        return total_length_m / 1000


@dataclass
class LineSegment(Asset):
    voltage_kV: float
    length_m: float
    conductor_type: str
    conductor_size_mm2: float
    status: str = "ENERGIZED"
    feeder: Optional[Feeder] = None
    # terminal_pole: Optional["Pole"] = None
    poles: List["Pole"] = field(default_factory=list)


@dataclass
class Pole(Asset):
    pole_number: str
    material: str
    height_m: float
    installation_year: int
    mounted_assets: List[Asset] = field(default_factory=list)


@dataclass
class Switch(Asset):
    switch_type: str
    status: str
    normally_closed: bool
    voltage_kV: float
    mounted_on: Optional[Pole] = None


@dataclass
class Transformer(Asset):
    rating_kVA: float
    primary_voltage: float
    secondary_voltage: float
    vector_group: str
    cooling: str
    mounted_on: Optional[Pole] = None
    customers: List["Customer"] = field(default_factory=list)

@dataclass
class Customer(Asset):
    customer_type: str
    load_kW: float
    transformer: Optional[Transformer] = None