# """
# VoltMap → IEC CIM mapping.
# """

# from models import (
#     Substation,
#     Feeder,
#     LineSegment,
#     Pole,
#     Switch,
#     Transformer,
#     Customer,
# )

# from .profile import CIMClass


# CIM_MAPPING = {
#     Substation: CIMClass.SUBSTATION,
#     Feeder: CIMClass.FEEDER,
#     LineSegment: CIMClass.AC_LINE_SEGMENT,
#     Pole: CIMClass.POLE,
#     Switch: CIMClass.SWITCH,
#     Transformer: CIMClass.POWER_TRANSFORMER,
#     Customer: CIMClass.ENERGY_CONSUMER,
# }

# def cim_class(asset):

#     return CIM_MAPPING[type(asset)]

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
    return MODEL_TO_CIM[type(asset)]

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