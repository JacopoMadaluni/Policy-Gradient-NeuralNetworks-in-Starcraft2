from .units import initialize_units
from .units import initialize_units_agent
from .logic import getLogic

def init_logic_modules(agent):
    initialize_units(getLogic(agent)) # magic lines
    initialize_units_agent(agent)
