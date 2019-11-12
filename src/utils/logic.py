from sc2.constants import PROBE, ZEALOT, SENTRY, STALKER, ADEPT, HIGHTEMPLAR, DARKTEMPLAR, ARCHON, OBSERVER, WARPPRISM, IMMORTAL, \
                        COLOSSUS, DISRUPTOR, PHOENIX, VOIDRAY, ORACLE, TEMPEST, CARRIER, MOTHERSHIP

from sc2.constants import NEXUS, PYLON, ASSIMILATOR, GATEWAY, FORGE, CYBERNETICSCORE, SHIELDBATTERY, TWILIGHTCOUNCIL, ROBOTICSFACILITY, \
                    STARGATE, TEMPLARARCHIVE, ROBOTICSBAY, DARKSHRINE, PHOTONCANNON, FLEETBEACON                        

from sc2.constants import MARINE, MARAUDER, REAPER, GHOST, HELLION, WIDOWMINE, SIEGETANK, CYCLONE, THOR, VIKING, MEDIVAC, LIBERATOR, \
                        BANSHEE, RAVEN, BATTLECRUISER

from .notifier import Notifier
class Logic:

    def __init__(self, agent):
        self.agent = agent



    async def buildStructure(self, structure, postAction=None, plan=False, pylon=None):
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

    async def buildColossus(self):
        agent = self.agent
        # TODO for loop ?
        for roboticsFacility in agent.units(ROBOTICSFACILITY).ready.idle:
            if (agent.units(ROBOTICSBAY).ready.exists and agent.can_afford(COLOSSUS) and 
                    agent.supply_left >= 4):
                await agent.do(roboticsFacility.train(COLOSSUS))
                return True
        return False        


    def canBuildColossus(self):
        return self.agent.units(ROBOTICSBAY).ready.exists and self.agent.units(ROBOTICSFACILITY).ready.exists

logic = None
def getLogic(agent):
    global logic
    if not logic:
        logic = Logic(agent)
    return logic         