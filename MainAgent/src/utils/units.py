
from .constants import *
from .logic import getLogic
#import sc2.constants

class Units():

    def set_agent(self, agent):
        self.agent = agent

    def generate_protoss_drawing_order(self):
        final_order = []
        for unit_type in self.protossUnits:
            if len(final_order) == 0:
                final_order.append(unit_type)
            else:    
                size = self.protossUnits[unit_type]["visualization"]["size"]
                for i, e in enumerate(final_order):
                    inserted = False
                    other_size = self.protossUnits[e]["visualization"]["size"]
                    if other_size <= size:
                        final_order.insert(i, unit_type)
                        inserted = True
                        break
                if not inserted:
                    final_order.append(unit_type)     
        return final_order                          
            

    def generate_terran_drawing_order(self):
        final_order = []
        for unit_type in self.terran_units:
            if len(final_order) == 0:
                final_order.append(unit_type)
            else:    
                size = self.terran_units[unit_type]["visualization"]["size"]
                for i, e in enumerate(final_order):
                    inserted = False
                    other_size = self.terran_units[e]["visualization"]["size"]
                    if other_size <= size:
                        final_order.insert(i, unit_type)
                        inserted = True
                        break
                if not inserted:
                    final_order.append(unit_type)        
        return final_order                          



            

    def initialize(self, logic):
        self.logic = logic
        
        self.protossUnits = self.get_protoss_units()
        self.terran_units = self.get_terran_units()

        self.protoss_drawing_order = self.generate_protoss_drawing_order()
        self.terran_drawing_order  = self.generate_terran_drawing_order()

    def get_protoss_units(self):
        return {
            PROBE: {
                "type": "unit",
                "supply": 1,
                "counters": set([]),
                "builtIn": NEXUS,
                "canBuildFunction": lambda: self.logic.can_build(PROBE),
                "required": None,
                "visualization": {
                    "color": (100, 200, 0), # BGR
                    "size": 1
                }
            }, 
            ZEALOT : {
                "type": "unit",
                "supply": 2,
                "counters": set([MARINE, HELLION]),
                "builtIn": GATEWAY,
                "canBuildFunction": lambda: self.logic.can_build(ZEALOT),
                "required": None,
                "visualization": {
                    "color": (40, 176, 0),
                    "size": 1
                }
            },
            ADEPT: {
                "type": "unit",
                "supply": 2,
                "counters": set([MARAUDER, SIEGETANK, CYCLONE]),
                "builtIn": GATEWAY,
                "canBuildFunction": lambda: self.logic.can_build(ADEPT),
                "required": CYBERNETICSCORE,
                "visualization": {
                    "color": (50, 210, 0),
                    "size": 1
                }
            },
            SENTRY: {
                "type": "unit",
                "supply": 2,
                "counters": set([HELLION, BANSHEE, SIEGETANK]),
                "builtIn": GATEWAY,
                "canBuildFunction": lambda: self.logic.can_build(SENTRY),
                "required": CYBERNETICSCORE,
                "visualization": {
                    "color": (148, 210, 0),
                    "size": 1
                }
            },
            STALKER: {
                "type": "unit",
                "supply": 2,
                "counters": set([MARAUDER, SIEGETANK]),
                "builtIn": GATEWAY,
                "canBuildFunction": lambda: self.logic.can_build(STALKER),
                "required": CYBERNETICSCORE,
                "visualization": {
                    "color": (55, 230, 0),
                    "size": 1
                }
            },
            HIGHTEMPLAR: {
                "type": "unit",
                "supply": 2,
                "counters": set([SIEGETANK, GHOST]),
                "builtIn": GATEWAY,
                "canBuildFunction": lambda: self.logic.can_build(HIGHTEMPLAR),
                "required": TEMPLARARCHIVE,
                "visualization": {
                    "color": (75, 230, 0),
                    "size": 1
                }
            },
            DARKTEMPLAR: {
                "type": "unit",
                "supply": 2,
                "counters": set([SIEGETANK, BANSHEE]),
                "builtIn": GATEWAY,
                "canBuildFunction": lambda: self.logic.can_build(DARKTEMPLAR),
                "required": DARKSHRINE,
                "visualization": {
                    "color": (48, 144, 0),
                    "size": 1
                }
            },
            ARCHON: {
                "type": "unit",
                "supply": 0,
                "counters": set([]),
                "builtIn": None,
                "canBuildFunction": self.logic.can_build_archon,
                "required": TEMPLARARCHIVE,
                "visualization": {
                    "color": (247, 255, 169),
                    "size": 2
                }
            },
            IMMORTAL: {
                "type": "unit",
                "supply": 4,
                "counters": set([MARINE, GHOST]),
                "builtIn": ROBOTICSFACILITY,
                "canBuildFunction": lambda: self.logic.can_build(IMMORTAL),
                "required": None,
                "visualization": {
                    "color": (55, 250, 0),
                    "size": 1
                }
            },
            COLOSSUS: {
                "type": "unit",
                "supply": 6,
                "counters": set([SIEGETANK, VIKING]),
                "builtIn": ROBOTICSFACILITY,
                "buildFunction": lambda: self.logic.build_unit(COLOSSUS),
                "canBuildFunction": lambda: self.logic.can_build(COLOSSUS),
                "required": ROBOTICSBAY,
                "visualization": {
                    "color": (105, 208, 0),
                    "size": 2
                }
            },
            OBSERVER: {
                "type": "unit",
                "supply": 1,
                "counters": set([]),
                "builtIn": ROBOTICSFACILITY,
                "buildFunction": lambda: self.logic.build_unit(OBSERVER),
                "canBuildFunction": lambda: self.logic.can_build(OBSERVER),
                "required": ROBOTICSFACILITY,
                "visualization": {
                    "color": (255, 255, 255),
                    "size": 1
                }
            },
            NEXUS: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "required": None,
                "visualization": {
                    "color": (0, 255, 0),
                    "size": 15
                }
            },
            PYLON: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "canBuildFunction": lambda: self.agent.units(NEXUS).ready.exists,
                "required": NEXUS,
                "visualization": {
                    "color": (20, 235, 0),
                    "size": 2
                }
            },
            ASSIMILATOR:{
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "required": NEXUS,
                "visualization": {
                    "color": (55, 200, 0),
                    "size": 2
                }
            },
            GATEWAY: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "canBuildFunction": lambda: self.agent.units(PYLON).ready.exists,
                "required": PYLON,
                "visualization": {
                    "color": (200, 100, 0),
                    "size": 2
                }                
            },
            FORGE: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "required": PYLON,
                "visualization": {
                    "color": (170, 150, 0),
                    "size": 2
                } 
            },
            CYBERNETICSCORE: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "canBuildFunction": lambda: self.agent.units(GATEWAY).ready.exists,
                "required": GATEWAY,
                "visualization": {
                    "color": (150, 150, 0),
                    "size": 2
                } 
            },
            SHIELDBATTERY: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "required": CYBERNETICSCORE,
                "visualization": {
                    "color": (100, 150, 0),
                    "size": 2
                } 
            },
            PHOTONCANNON: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "required": FORGE,
                "visualization": {
                    "color": (200, 250, 0),
                    "size": 2
                } 
            },
            TWILIGHTCOUNCIL: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "required": CYBERNETICSCORE,
                "visualization": {
                    "color": (200, 170, 0),
                    "size": 2
                } 
            },
            ROBOTICSFACILITY: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "canBuildFunction": lambda: self.agent.units(CYBERNETICSCORE).ready.exists,
                "required": CYBERNETICSCORE,
                "visualization": {
                    "color": (215, 155, 0),
                    "size": 2
                } 
            },
            STARGATE: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "required": CYBERNETICSCORE,
                "visualization": {
                    "color": (255, 0, 0),
                    "size": 2
                } 
            },
            TEMPLARARCHIVE: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "required": TWILIGHTCOUNCIL,
                "visualization": {
                    "color": (210, 180, 0),
                    "size": 2
                } 
            },
            DARKSHRINE: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "required": TWILIGHTCOUNCIL,
                "visualization": {
                    "color": (180, 100, 0),
                    "size": 2
                } 
            },
            ROBOTICSBAY: {
                "type": "structure",
                "buildFunction": self.logic.build_structure,
                "canBuildFunction": lambda: self.agent.units(ROBOTICSFACILITY).ready.exists, 
                "required": ROBOTICSFACILITY,
                "visualization": {
                    "color": (235, 185, 0),
                    "size": 2
                } 
            },
            FLEETBEACON: {
                "type": "structure",
                "buildFunction": self.logic.build_structure, # TODO lambda: self.logic.build_structure(STRUCTURE) ..
                "required": STARGATE,
                "visualization": {
                    "color": (275, 0, 0),
                    "size": 2
                } 
            }
        }    
    def get_terran_units(self):
        return {
            SCV: {
                "counters": set(),
                "visualization":{
                    "color": (55, 0, 200),
                    "size": 1
                }
            },
            MULE: {
                "counters": set(),
                "visualization":{
                    "color": (65, 0, 210),
                    "size": 1
                }
            },
            MARINE: {
                "counters": set([COLOSSUS]),
                "visualization":{
                    "color": (55, 0, 155),
                    "size": 1
                }
            },
            MARAUDER: {
                "counters": set([IMMORTAL, VOIDRAY, ZEALOT]),
                "visualization":{
                    "color": (55, 0, 175),
                    "size": 1
                }
            },
            REAPER: {
                "counters": set([STALKER]),
                "visualization":{
                    "color": (35, 0, 155),
                    "size": 1
                }
            },
            GHOST: {
                "counters": set([STALKER]),
                "visualization":{
                    "color": (55, 0, 185),
                    "size": 1
                }
            },
            HELLION: {
                "counters": set([STALKER]),
                "visualization":{
                    "color": (35, 0, 135),
                    "size": 1
                }
            },
            SIEGETANK: {
                "counters": set([IMMORTAL, VOIDRAY]),
                "visualization":{
                    "color": (25, 0, 105),
                    "size": 1
                }
            },
            THOR: {
                "counters": set([IMMORTAL]),
                "visualization":{
                    "color": (0, 0, 105),
                    "size": 1
                }
            },
            BANSHEE: {
                "counters": set([VOIDRAY]),
                "visualization":{
                    "color": (100, 0, 200),
                    "size": 1
                }           
            },
            VIKING: {
                "counters": set([STALKER]),
                "visualization":{
                    "color": (100, 0, 180),
                    "size": 1
                }  
            },
            VIKINGFIGHTER: {
                "counters": set([STALKER]),
                "visualization":{
                    "color": (110, 0, 190),
                    "size": 1
                }  
            },
            RAVEN: {
                "counters": set([STALKER]),
                "visualization":{
                    "color": (141, 0, 235),
                    "size": 1
                }  
            },
            MEDIVAC: {
                "counters": set([STALKER, VOIDRAY]),
                "visualization":{
                    "color": (141, 0, 255),
                    "size": 1
                } 
            },
            BATTLECRUISER: {
                "counters": set([VOIDRAY]),
                "visualization":{
                    "color": (0, 0, 255),
                    "size": 1
                }
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