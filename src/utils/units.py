import asyncio

from sc2.constants import PROBE, ZEALOT, SENTRY, STALKER, ADEPT, HIGHTEMPLAR, DARKTEMPLAR, ARCHON, OBSERVER, WARPPRISM, IMMORTAL, \
                        COLOSSUS, DISRUPTOR, PHOENIX, VOIDRAY, ORACLE, TEMPEST, CARRIER, MOTHERSHIP

from sc2.constants import NEXUS, PYLON, ASSIMILATOR, GATEWAY, FORGE, CYBERNETICSCORE, SHIELDBATTERY, TWILIGHTCOUNCIL, ROBOTICSFACILITY, \
                    STARGATE, TEMPLARARCHIVE, ROBOTICSBAY, DARKSHRINE, PHOTONCANNON, FLEETBEACON                        

from sc2.constants import MARINE, MARAUDER, REAPER, GHOST, HELLION, WIDOWMINE, SIEGETANK, CYCLONE, THOR, VIKING, MEDIVAC, LIBERATOR, \
                        BANSHEE, RAVEN, BATTLECRUISER

from .logic import Logic
#import sc2.constants

class Units():

    def test(self):
        if True:
            return "good"

    def __init__(self, agent):
        self.agent = agent
        self.logic = Logic(self.agent)
        self.protossUnits = {
            PROBE: {
                "type": "unit",
                "counters": set([]),
                "builtIn": NEXUS,
                "canBuildFunction": self.logic.canBuildColossus,
                "required": None
            }, 
            ZEALOT : {
                "type": "unit",
                "counters": set([MARINE, HELLION]),
                "builtIn": GATEWAY,
                "canBuildFunction": self.logic.canBuildColossus,
                "required": None
            },
            ADEPT: {
                "type": "unit",
                "counters": set([MARAUDER, SIEGETANK, CYCLONE]),
                "builtIn": GATEWAY,
                "canBuildFunction": self.logic.canBuildColossus,
                "required": CYBERNETICSCORE
            },
            SENTRY: {
                "type": "unit",
                "counters": set([HELLION, BANSHEE, SIEGETANK]),
                "builtIn": GATEWAY,
                "canBuildFunction": self.logic.canBuildColossus,
                "required": CYBERNETICSCORE
            },
            STALKER: {
                "type": "unit",
                "counters": set([MARAUDER, SIEGETANK]),
                "builtIn": GATEWAY,
                "canBuildFunction": self.logic.canBuildColossus,
                "required": CYBERNETICSCORE
            },
            HIGHTEMPLAR: {
                "type": "unit",
                "counters": set([SIEGETANK, GHOST]),
                "builtIn": GATEWAY,
                "canBuildFunction": self.logic.canBuildColossus,
                "required": TEMPLARARCHIVE
            },
            DARKTEMPLAR: {
                "type": "unit",
                "counters": set([SIEGETANK, BANSHEE]),
                "builtIn": GATEWAY,
                "canBuildFunction": self.logic.canBuildColossus,
                "required": DARKSHRINE
            },
            ARCHON: {
                "type": "unit",
                "counters": set([]),
                "builtIn": self.test,
                "canBuildFunction": self.logic.canBuildColossus,
                "required": TEMPLARARCHIVE
            },
            IMMORTAL: {
                "type": "unit",
                "counters": set([MARINE, GHOST]),
                "builtIn": ROBOTICSFACILITY,
                "canBuildFunction": self.logic.canBuildColossus,
                "required": None
            },
            COLOSSUS: {
                "type": "unit",
                "counters": set([SIEGETANK, VIKING]),
                "buildFunction": self.logic.buildColossus,
                "canBuildFunction": self.logic.canBuildColossus,
                "required": ROBOTICSBAY
            },
            NEXUS: {
                "type": "structure",
                "buildFunction": self.logic.buildStructure,
                "required": None
            },
            PYLON: {
                "type": "structure",
                "buildFunction": self.logic.buildStructure,
                "canBuildFunction": lambda: agent.units(NEXUS).ready.exists,
                "required": NEXUS
            },
            ASSIMILATOR:{
                "type": "structure",
                "buildFunction": self.logic.buildStructure,
                "required": NEXUS
            },
            GATEWAY: {
                "type": "structure",
                "buildFunction": self.logic.buildStructure,
                "canBuildFunction": lambda: agent.units(PYLON).ready.exists,
                "required": PYLON
            },
            FORGE: {
                "type": "structure",
                "buildFunction": self.logic.buildStructure,
                "required": PYLON
            },
            CYBERNETICSCORE: {
                "type": "structure",
                "buildFunction": self.logic.buildStructure,
                "canBuildFunction": lambda: agent.units(GATEWAY).ready.exists,
                "required": GATEWAY
            },
            SHIELDBATTERY: {
                "type": "structure",
                "buildFunction": self.logic.buildStructure,
                "required": CYBERNETICSCORE
            },
            PHOTONCANNON: {
                "type": "structure",
                "buildFunction": self.logic.buildStructure,
                "required": FORGE
            },
            TWILIGHTCOUNCIL: {
                "type": "structure",
                "buildFunction": self.logic.buildStructure,
                "required": CYBERNETICSCORE
            },
            ROBOTICSFACILITY: {
                "type": "structure",
                "buildFunction": self.logic.buildStructure,
                "canBuildFunction": lambda: agent.units(CYBERNETICSCORE).ready.exists,
                "required": CYBERNETICSCORE
            },
            STARGATE: {
                "type": "structure",
                "buildFunction": self.logic.buildStructure,
                "required": CYBERNETICSCORE
            },
            TEMPLARARCHIVE: {
                "type": "structure",
                "buildFunction": self.logic.buildStructure,
                "required": TWILIGHTCOUNCIL
            },
            DARKSHRINE: {
                "type": "structure",
                "buildFunction": self.logic.buildStructure,
                "required": TWILIGHTCOUNCIL
            },
            ROBOTICSBAY: {
                "type": "structure",
                "buildFunction": self.logic.buildStructure,
                "canBuildFunction": lambda: agent.units(ROBOTICSFACILITY).ready.exists, 
                "required": ROBOTICSFACILITY
            },
            FLEETBEACON: {
                "type": "structure",
                "buildFunction": self.logic.buildStructure,
                "required": STARGATE
            }
        } 

        self.terranUnits = {
            MARINE: {
                "counters": set([COLOSSUS])
            },
            MARAUDER: {
                "counters": set([IMMORTAL, VOIDRAY, ZEALOT])
            },
            REAPER: {
                "counters": set([STALKER])
            },
            GHOST: {
                "counters": set([STALKER])
            },
            HELLION: {
                "counters": set([STALKER])
            },
            SIEGETANK: {
                "counters": set([IMMORTAL, VOIDRAY])
            },
            THOR: {
                "counters": set([IMMORTAL])
            },
            BANSHEE: {
                "counters": set([VOIDRAY])
            },
            VIKING: {
                "counters": set([STALKER])
            },
            RAVEN: {
                "counters": set([STALKER])
            },
            MEDIVAC: {
                "counters": set([STALKER, VOIDRAY])
            },
            BATTLECRUISER: {
                "counters": set([VOIDRAY])
            }
        }

units = None      
def getUnits(agent):
    global units
    if not units:
        units = Units(agent)
    return units    

if __name__ == "__main__":
    x = Units()
    print(x.protossUnits)
    f = x.protossUnits[ARCHON]["builtIn"]
    print(f())