# """
# Simplified IEC CIM profile supported by VoltMap.
# """

# from enum import Enum


# class CIMClass(str, Enum):
#     SUBSTATION = "Substation"
#     FEEDER = "Feeder"
#     AC_LINE_SEGMENT = "ACLineSegment"
#     POLE = "Pole"
#     SWITCH = "Switch"
#     POWER_TRANSFORMER = "PowerTransformer"
#     ENERGY_CONSUMER = "EnergyConsumer"
"""
IEC Common Information Model (CIM)
Supported profile for VoltMap.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CIMEntity:
    """
    Metadata describing a supported CIM class.
    """

    name: str
    package: str
    description: str
    relationships: Tuple[str, ...] = ()
    
SUBSTATION = CIMEntity(
    name="Substation",
    package="Core",
    description="A collection of equipment for distributing electrical energy.",
    relationships=("Feeder",)
)

FEEDER = CIMEntity(
    name="Feeder",
    package="Wires",
    description="A distribution feeder originating from a substation.",
    relationships=("ACLineSegment",)
)

AC_LINE_SEGMENT = CIMEntity(
    name="ACLineSegment",
    package="Wires",
    description="A section of AC overhead or underground conductor.",
    relationships=("Pole",)
)

POLE = CIMEntity(
    name="Pole",
    package="Assets",
    description="Utility pole supporting electrical equipment.",
    relationships=("Switch", "PowerTransformer")
)

SWITCH = CIMEntity(
    name="Switch",
    package="Wires",
    description="A switching device used for sectionalizing the network."
)

POWER_TRANSFORMER = CIMEntity(
    name="PowerTransformer",
    package="Wires",
    description="Distribution transformer."
)

ENERGY_CONSUMER = CIMEntity(
    name="EnergyConsumer",
    package="LoadModel",
    description="Electrical load connected to the distribution system."
)