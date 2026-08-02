"""
generator config    
"""

from dataclasses import dataclass


@dataclass(slots=True)
class GeneratorConfig:
    #network size
    num_substations: int = 2
    feeders_per_substation: int = 4
    line_segments_per_feeder: int = 15

    # Electrical parameters
    feeder_voltage_kv: float = 11.0
    substation_voltage_kv: float = 33.0

    # Randomness
    random_seed: int = 42

    # Metadata
    version: str = "1.0.0"