from .units import initialize_units
from .units import initialize_units_agent
from .logic import getLogic

def init_logic_modules(agent):
    """
    Executed at startup.
    Manually intializes key objects to avoid loops during import.
    """
    initialize_units(getLogic(agent)) # magic lines
    initialize_units_agent(agent)
