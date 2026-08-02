"""
VoltMap Engineering Rules
"""

# Voltage Levels
# SUBSTATION_VOLTAGE = 33
# FEEDER_VOLTAGE = 11
# SERVICE_VOLTAGE = 0.415

# Infrastructure Placement Rules
TRANSFORMER_INTERVAL = 5      # Every 5 poles
SECTION_SWITCH_INTERVAL = 10  # Every 10 poles

# Customer Rules
MIN_CUSTOMERS = 15
MAX_CUSTOMERS = 35

# Line Rules

MIN_LINE_LENGTH = 80      # metres
MAX_LINE_LENGTH = 250

# Pole Rules

DEFAULT_POLE_HEIGHT = 12
POLE_MATERIAL = "Concrete"

CUSTOMER_LOADS = {
    "Residential": (1.5, 5.0),
    "Commercial": (5.0, 30.0),
    "Institutional": (20.0, 100.0),
    "Healthcare": (15.0, 80.0),
    "Government": (25.0, 120.0),
    "Religious": (5.0, 20.0),
    "Utility": (20.0, 150.0)
}