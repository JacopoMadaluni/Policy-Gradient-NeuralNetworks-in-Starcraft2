from .constants import *
from .notifier import Notifier

class Logic:

    def __init__(self, agent):
        from .units import getUnits
        self.agent = agent
        self.units = getUnits()

    def post_action(function):
        async def f(*args, **kwargs):
            return_value = function(*args, **kwargs)
            if return_value and "postAction" in kwargs:
                kwargs["postAction"]()
            if not return_value and "failureAction" in kwargs:
                kwargs["failureAction"]()    
            return return_value
        return f         



    async def build_structure(self, structure, postAction=None, plan=False, pylon=None):
        agent = self.agent
        #if plan and agent.units(structure).not_ready.exists:
        #    return 2
        
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

    """async def build_colossus(self):
        agent = self.agent
        # TODO for loop ?
        for roboticsFacility in agent.units(ROBOTICSFACILITY).ready.idle:
            if (agent.units(ROBOTICSBAY).ready.exists and agent.can_afford(COLOSSUS) and 
                    agent.supply_left >= 4):
                await agent.do(roboticsFacility.train(COLOSSUS))
                return True
        return False    """

    async def build_unit(self, unit):
        agent = self.agent
        supply_needed = self.units.protossUnits[unit]["supply"]
        target_structure = self.units.protossUnits[unit]["builtIn"]
        for structure in agent.units(target_structure).ready.idle:
            if (agent.can_afford(unit) and
                agent.supply_left >= supply_needed):
                await agent.do(target_structure.train(unit))
                return True
        return False       

    def can_build_archon(self):
        # TODO obvs
        return False     



    def can_build(self, unit):
        structure_required = self.units.protossUnits[unit]["builtIn"]
        tech_required = self.units.protossUnits[unit]["required"]
        if tech_required:
            return self.agent.units(structure_required).ready.exists and self.agent.units(tech_required).ready.exists
        else:
            return self.agent.units(structure_required).ready.exists  

logic = None
def getLogic(agent):
    global logic
    if not logic:
        logic = Logic(agent)
    return logic         