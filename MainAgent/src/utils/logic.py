import random
from .constants import *
from .notifier import Notifier
from .function_utils import agent_method

class Logic:
    """
    The main logic resides in this class.
    All default functions to produce units and structures resides in this class.
    """
    def __init__(self, agent):
        from .units import getUnits
        self.agent = agent
        self.units = getUnits()

 
    async def build_structure(self, structure, postAction=None, pylon=None):
        """
        Main function to build a structure.
        If a post action is specified, it will be executed when the structure is 
        finished building.

        Inputs:
           structure:  the id of the structure to be built
           postaction: action to be done after the structure is finished building (can be None)
           pylon: pylon to build the new structure (can be None) 
        """

        agent = self.agent
        
        if agent.units(PYLON).ready.exists:
            if not pylon:
                pylon = agent.units(PYLON).ready.random    
            if agent.can_afford(structure):
                await agent.build(structure, near=pylon)
                if postAction:
                    condition = lambda: agent.units(structure).ready.exists
                    notifier = Notifier(condition, postAction)
                    notifier.start()
                return True
        return False        

    @agent_method
    def choose_structure_to_train(self, structure_type, agent=None):
        """
        Returns a random idle structure of the specified type.
        If there are no idle structures of the specified type, it returns None.
        """
        available_structures = agent.units(structure_type).ready.idle
        if not available_structures:
            return None
        else:
            return random.choice(available_structures)    

    @agent_method
    async def build_unit(self, unit, agent=None):
        """
        Main function to train a unit.
        Returns True if the train command was executed, false otherwise.

        The train command will not be executed if (or):
            - there is no available structure to train the selected unit
            - the agent cannot afford the selected unit
            - the agent does not have enough supply for the selected unit
        """
        supply_needed = self.units.protossUnits[unit]["supply"]
        target_structure = self.choose_structure_to_train(self.units.protossUnits[unit]["builtIn"])
        if target_structure:
            if (agent.can_afford(unit) and agent.supply_left >= supply_needed):
                await agent.do(target_structure.train(unit))
                return True
        return False

    @agent_method
    async def warp_unit(self, unit, agent=None):
        """
        Main function to warp a unit.
        Warping a unit is equivalent of training a unit. The warped unit will be spawned 
        near a chosen pylon instead of spawning near the structure that trained it.

        This method warps the selected units near a random pylon.
        """
        if agent.units(PYLON):
            pylon = random.choice(agent.units(PYLON))
            for warpgate in agent.units(WARPGATE).ready:
                can_warp = await agent.get_available_abilities(warpgate)
                warp_ability = self.units.protossUnits[unit]["warpAbilityId"]
                if warp_ability in can_warp:
                    warp_location = pylon.position.to2.random_on_distance(4)
                    placement = await agent.find_placement(warp_ability, warp_location, placement_step=1)
                    if placement is None:
                        print("could not warp")
                        return
                    await agent.do(warpgate.warp_in(unit, placement)) 

    @agent_method
    async def build_gateway_unit(self, unit, agent=None):
        """
        Since gateway units can be both trained or warped, 
        this method warps the selected unit if possible, otherwise
        it trains it.
        """ 
        if len(agent.units(WARPGATE).ready) != 0:
            # warpgate was researched hence the unit must be warped
            await self.warp_unit(unit)
              
        if len(agent.units(GATEWAY).ready.noqueue) != 0:
            await self.build_unit(unit)


    def can_build_archon(self):
        # TODO obvs
        return False     



    def can_build(self, unit):
        """
        Returns True if the input unit can be built.
        A specified unit can be build if:
            - the agent has the required structure, and
            - the agent has the tech required to build the unit
        """
        structure_required = self.units.protossUnits[unit]["builtIn"]
        tech_required = self.units.protossUnits[unit]["required"]
        if tech_required:
            return self.agent.units(structure_required).ready.exists and self.agent.units(tech_required).ready.exists
        else:
            return self.agent.units(structure_required).ready.exists  

logic = None
def getLogic(agent):
    """
    Singleton pattern, returns the logic singleton object
    """
    global logic
    if not logic:
        logic = Logic(agent)
    return logic         