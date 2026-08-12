"""
VoltMap → IEC CIM mapping.
"""

from .profile import (
    SUBSTATION,
    FEEDER,
    AC_LINE_SEGMENT,
    POLE,
    SWITCH,
    POWER_TRANSFORMER,
    ENERGY_CONSUMER,
)

from generator.models import (
    Substation,
    Feeder,
    LineSegment,
    Pole,
    Switch,
    Transformer,
    Customer,
)

MODEL_TO_CIM = {
    Substation: SUBSTATION,
    Feeder: FEEDER,
    LineSegment: AC_LINE_SEGMENT,
    Pole: POLE,
    Switch: SWITCH,
    Transformer: POWER_TRANSFORMER,
    Customer: ENERGY_CONSUMER,
}

def cim_entity(asset):
    """
    Get the CIM entity corresponding to a VoltMap asset.
    """
    try:
        return MODEL_TO_CIM[type(asset)]
    except KeyError as e:
        raise ValueError(f"No CIM mapping defined for asset type: {type(asset).__name__}") from e

def cim_name(asset):
    """
    Get the CIM class name corresponding to a VoltMap asset.
    """
    return cim_entity(asset).name

def cim_package(asset):
    """
    Get the CIM package name corresponding to a VoltMap asset.
    """
    return cim_entity(asset).package