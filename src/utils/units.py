from sc2.constants import PROBE, ZEALOT, SENTRY, STALKER, ADEPT, HIGHTEMPLAR, DARKTEMPLAR, ARCHON, OBSERVER, WARPPRISM, IMMORTAL, \
                        COLOSSUS, DISRUPTOR, PHOENIX, VOIDRAY, ORACLE, TEMPEST, CARRIER, MOTHERSHIP

from sc2.constants import NEXUS, PYLON, ASSIMILATOR, GATEWAY, FORGE, CYBERNETICSCORE, SHIELDBATTERY, TWILIGHTCOUNCIL, ROBOTICSFACILITY, \
                    STARGATE, TEMPLARARCHIVE, ROBOTICSBAY, DARKSHRINE, PHOTONCANNON, FLEETBEACON                        

from sc2.constants import MARINE, MARAUDER, REAPER, GHOST, HELLION, WIDOWMINE, SIEGETANK, CYCLONE, THOR, VIKING, MEDIVAC, LIBERATOR, \
                        BANSHEE, RAVEN, BATTLECRUISER

from .logic import getLogic
#import sc2.constants

class Units():

    def set_agent(self, agent):
        self.agent = agent


    def initialize(self, logic):
        self.logic = logic
        self.protossUnits = {
            PROBE: {
                "type": "unit",
                "supply": 1,
                "counters": set([]),
                "builtIn": NEXUS,
                "canBuildFunction": lambda: self.logic.can_build(PROBE),
                "required": None
            }, 
            ZEALOT : {
                "type": "unit",
                "supply": 2,
                "counters": set([MARINE, HELLION]),
                "builtIn": GATEWAY,
                "canBuildFunction": lambda: self.logic.can_build(ZEALOT),
                "required": None
            },
            ADEPT: {
                "type": "unit",
                "supply": 2,
                "counters": set([MARAUDER, SIEGETANK, CYCLONE]),
                "builtIn": GATEWAY,
                "canBuildFunction": lambda: self.logic.can_build(ADEPT),
                "required": CYBERNETICSCORE
            },
            SENTRY: {
                "type": "unit",
                "supply": 2,
                "counters": set([HELLION, BANSHEE, SIEGETANK]),
                "builtIn": GATEWAY,
                "canBuildFunction": lambda: self.logic.can_build(SENTRY),
                "required": CYBERNETICSCORE
            },
            STALKER: {
                "type": "unit",
                "supply": 2,
                "counters": set([MARAUDER, SIEGETANK]),
                "builtIn": GATEWAY,
                "canBuildFunction": lambda: self.logic.can_build(STALKER),
                "required": CYBERNETICSCORE
            },
            HIGHTEMPLAR: {
                "type": "unit",
                "supply": 2,
                "counters": set([SIEGETANK, GHOST]),
                "builtIn": GATEWAY,
                "canBuildFunction": lambda: self.logic.can_build(HIGHTEMPLAR),
                "required": TEMPLARARCHIVE
            },
            DARKTEMPLAR: {
                "type": "unit",
                "supply": 2,
                "counters": set([SIEGETANK, BANSHEE]),
                "builtIn": GATEWAY,
                "canBuildFunction": lambda: self.logic.can_build(DARKTEMPLAR),
                "required": DARKSHRINE
            },
            ARCHON: {
                "type": "unit",
                "supply": 0,
                "counters": set([]),
                "builtIn": None,
                "canBuildFunction": self.logic.can_build_archon,
                "required": TEMPLARARCHIVE
            },
            IMMORTAL: {
                "type": "unit",
                "supply": 4,
                "counters": set([MARINE, GHOST]),
                "builtIn": ROBOTICSFACILITY,
                "canBuildFunction": lambda: self.logic.can_build(IMMORTAL),
                "required": None
            },
            COLOSSUS: {
                "type": "unit",
                "supply": 6,
                "counters": set([SIEGETANK, VIKING]),
                "builtIn": ROBOTICSFACILITY,
                "buildFunction": lambda: self.logic.build_unit(COLOSSUS),
                "canBuildFunction": lambda: self.logic.can_build(COLOSSUS),
                "required": ROBOTICSBAY
            },
            OBSERVER: {
                "type": "unit",
                "supply": 1,
                "counters": set([]),
                "builtIn": ROBOTICSFACILITY,
                "buildFunction": lambda: self.logic.build_unit(OBSERVER),
                "canBuildFunction": lambda: self.logic.can_build(OBSERVER),
                "required": ROBOTICSFACILITY
            },
            NEXUS: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "required": None
            },
            PYLON: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "canBuildFunction": lambda: self.agent.units(NEXUS).ready.exists,
                "required": NEXUS
            },
            ASSIMILATOR:{
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "required": NEXUS
            },
            GATEWAY: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "canBuildFunction": lambda: self.agent.units(PYLON).ready.exists,
                "required": PYLON
            },
            FORGE: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "required": PYLON
            },
            CYBERNETICSCORE: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "canBuildFunction": lambda: self.agent.units(GATEWAY).ready.exists,
                "required": GATEWAY
            },
            SHIELDBATTERY: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "required": CYBERNETICSCORE
            },
            PHOTONCANNON: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "required": FORGE
            },
            TWILIGHTCOUNCIL: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "required": CYBERNETICSCORE
            },
            ROBOTICSFACILITY: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "canBuildFunction": lambda: self.agent.units(CYBERNETICSCORE).ready.exists,
                "required": CYBERNETICSCORE
            },
            STARGATE: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "required": CYBERNETICSCORE
            },
            TEMPLARARCHIVE: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "required": TWILIGHTCOUNCIL
            },
            DARKSHRINE: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "required": TWILIGHTCOUNCIL
            },
            ROBOTICSBAY: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "canBuildFunction": lambda: self.agent.units(ROBOTICSFACILITY).ready.exists, 
                "required": ROBOTICSFACILITY
            },
            FLEETBEACON: {
                "type": "structure",
                "buildFunction": self.logic.build_structure, # TODO lambda: self.logic.build_structure(STRUCTURE) ..
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

        

units = Units()      
initialized = False
def initialize_units(logic):
    units.initialize(logic) 

def initialize_units_agent(agent):
    units.set_agent(agent) 

def getUnits():
    return units

if __name__ == "__main__":
    x = Units()
    print(x.protossUnits)
    f = x.protossUnits[ARCHON]["builtIn"]
    print(f())