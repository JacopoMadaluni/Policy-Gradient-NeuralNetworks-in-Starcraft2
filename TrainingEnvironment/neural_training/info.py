# TERRAN UNITS
from sc2.constants import SCV, MULE, MARINE, MARAUDER, REAPER, GHOST, HELLION, WIDOWMINE, SIEGETANK, \
                        CYCLONE, HELLIONTANK, THOR, VIKING, VIKINGFIGHTER, MEDIVAC, LIBERATOR, \
                        BANSHEE, RAVEN, BATTLECRUISER

# TOSS UNITS
from sc2.constants import PROBE, ZEALOT, SENTRY, STALKER, ADEPT, HIGHTEMPLAR, DARKTEMPLAR, ARCHON, OBSERVER, WARPPRISM, IMMORTAL, \
                        COLOSSUS, DISRUPTOR, PHOENIX, VOIDRAY, ORACLE, TEMPEST, CARRIER, MOTHERSHIP                        
def terran_units():
    return {
                SCV: {
                    "counters": set(),
                    "visualization":{
                        "color": (55, 0, 200),
                        "size": 1
                    },
                    "supply": 1
                },
                MULE: {
                    "counters": set(),
                    "visualization":{
                        "color": (65, 0, 210),
                        "size": 1
                    },
                    "supply": 0
                },
                MARINE: {
                    "counters": set([COLOSSUS]),
                    "visualization":{
                        "color": (55, 0, 155),
                        "size": 1
                    },
                    "supply": 1
                },
                MARAUDER: {
                    "counters": set([IMMORTAL, VOIDRAY, ZEALOT]),
                    "visualization":{
                        "color": (55, 0, 175),
                        "size": 1
                    },
                    "supply": 2
                },
                REAPER: {
                    "counters": set([STALKER]),
                    "visualization":{
                        "color": (35, 0, 155),
                        "size": 1
                    },
                    "supply": 1
                },
                GHOST: {
                    "counters": set([STALKER]),
                    "visualization":{
                        "color": (55, 0, 185),
                        "size": 1
                    },
                    "supply": 2
                },
                HELLION: {
                    "counters": set([STALKER]),
                    "visualization":{
                        "color": (35, 0, 135),
                        "size": 1
                    },
                    "supply": 2
                },
                HELLIONTANK: {
                    "supply": 2
                },
                SIEGETANK: {
                    "counters": set([IMMORTAL, VOIDRAY]),
                    "visualization":{
                        "color": (25, 0, 105),
                        "size": 1
                    },
                    "supply": 3
                },
                THOR: {
                    "counters": set([IMMORTAL]),
                    "visualization":{
                        "color": (0, 0, 105),
                        "size": 1
                    },
                    "supply": 6
                },
                BANSHEE: {
                    "counters": set([VOIDRAY]),
                    "visualization":{
                        "color": (100, 0, 200),
                        "size": 1
                    },
                    "supply": 3           
                },
                VIKING: {
                    "counters": set([STALKER]),
                    "visualization":{
                        "color": (100, 0, 180),
                        "size": 1
                    },
                    "supply": 2  
                },
                VIKINGFIGHTER: {
                    "counters": set([STALKER]),
                    "visualization":{
                        "color": (110, 0, 190),
                        "size": 1
                    },
                    "supply": 2  
                },
                RAVEN: {
                    "counters": set([STALKER]),
                    "visualization":{
                        "color": (141, 0, 235),
                        "size": 1
                    },
                    "supply": 2  
                },
                MEDIVAC: {
                    "counters": set([STALKER, VOIDRAY]),
                    "visualization":{
                        "color": (141, 0, 255),
                        "size": 1
                    },
                    "supply": 2
                },
                BATTLECRUISER: {
                    "counters": set([VOIDRAY]),
                    "visualization":{
                        "color": (0, 0, 255),
                        "size": 1
                    },
                    "supply": 6
                }
            }