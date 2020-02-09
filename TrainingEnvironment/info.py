# TERRAN UNITS
from sc2.constants import SCV, MULE, MARINE, MARAUDER, REAPER, GHOST, HELLION, WIDOWMINE, SIEGETANK, \
                        CYCLONE, HELLIONTANK, THOR, VIKING, VIKINGFIGHTER, MEDIVAC, LIBERATOR, \
                        BANSHEE, RAVEN, BATTLECRUISER

# TOSS UNITS
from sc2.constants import PROBE, ZEALOT, SENTRY, STALKER, ADEPT, HIGHTEMPLAR, DARKTEMPLAR, ARCHON, OBSERVER, WARPPRISM, IMMORTAL, \
                        COLOSSUS, DISRUPTOR, PHOENIX, VOIDRAY, ORACLE, TEMPEST, CARRIER, MOTHERSHIP

def get_protoss_units():
        return {
            PROBE: {
                "supply": 1,
                "counters": set([]),
                "counteredby":set([]), # to be fixed in other entries
                "utility_against":{
                    MARINE: -10,
                    MARAUDER: -10,
                    REAPER: -10,
                    GHOST: -10,
                    HELLION: -10,
                    WIDOWMINE: -10,
                    SIEGETANK: -10,
                    CYCLONE: -10,
                    HELLIONTANK: -10,
                    THOR: -10,
                    VIKING: -10,
                    VIKINGFIGHTER: -10,
                    MEDIVAC: -10,
                    LIBERATOR: -10,
                    BANSHEE: -10,
                    RAVEN: -10,
                    BATTLECRUISER: -10
                }
            },
            ZEALOT : {
                "supply": 2,
                "counters": set([MARINE, HELLION]),
                "utility_against":{
                    MARINE: 5,
                    MARAUDER: 9,
                    REAPER: 6,
                    GHOST: -2,
                    HELLION: -4,
                    WIDOWMINE: -4,
                    SIEGETANK: 8,
                    CYCLONE: 8,
                    HELLIONTANK: -8,
                    THOR: 5,
                    VIKING: 0,
                    VIKINGFIGHTER: 6,
                    MEDIVAC: 0,
                    LIBERATOR: -9,
                    BANSHEE: -10,
                    RAVEN: -10,
                    BATTLECRUISER: -10
                }
            },
            ADEPT: {
                "supply": 2,
                "counters": set([MARAUDER, SIEGETANK, CYCLONE]),
                "utility_against":{
                    MARINE: 7,
                    MARAUDER: -6,
                    REAPER: 5,
                    GHOST: 5,
                    HELLION: -5,
                    WIDOWMINE: -6,
                    SIEGETANK: -8,
                    CYCLONE: -8,
                    HELLIONTANK: -7,
                    THOR: -9,
                    VIKING: 0,
                    VIKINGFIGHTER: -5,
                    MEDIVAC: 0,
                    LIBERATOR: -10,
                    BANSHEE: -10,
                    RAVEN: -10,
                    BATTLECRUISER: -10
                }
            },
            SENTRY: {
                "supply": 2,
                "counters": set([HELLION, BANSHEE, SIEGETANK]),
                "utility_against":{
                    MARINE: 0,
                    MARAUDER: 0,
                    REAPER: 0,
                    GHOST: 0,
                    HELLION: 0,
                    WIDOWMINE: 0,
                    SIEGETANK: 0,
                    CYCLONE: 0,
                    HELLIONTANK: 0,
                    THOR: 0,
                    VIKING: 0,
                    VIKINGFIGHTER: 0,
                    MEDIVAC: 0,
                    LIBERATOR: 0,
                    BANSHEE: 0,
                    RAVEN: 0,
                    BATTLECRUISER: 0
                }
            },
            STALKER: {

                "supply": 2,
                "counters": set([MARAUDER, SIEGETANK]),
                "utility_against":{
                    MARINE: 4,
                    MARAUDER: -5,
                    REAPER: 9,
                    GHOST: 8,
                    HELLION: 9,
                    WIDOWMINE: 3,
                    SIEGETANK: -8,
                    CYCLONE: -8,
                    HELLIONTANK: 8,
                    THOR: -2,
                    VIKING: 10,
                    VIKINGFIGHTER: 7,
                    MEDIVAC: 10,
                    LIBERATOR: 8,
                    BANSHEE: 7,
                    RAVEN: 10,
                    BATTLECRUISER: 7
                }
            },
            HIGHTEMPLAR: {
                "supply": 2,
                "counters": set([SIEGETANK, GHOST]),
                "utility_against":{
                    MARINE: 0,
                    MARAUDER: 0,
                    REAPER: 0,
                    GHOST: 0,
                    HELLION: 0,
                    WIDOWMINE: 0,
                    SIEGETANK: 0,
                    CYCLONE: 0,
                    HELLIONTANK: 0,
                    THOR: 0,
                    VIKING: 0,
                    VIKINGFIGHTER: 0,
                    MEDIVAC: 0,
                    LIBERATOR: 0,
                    BANSHEE: 0,
                    RAVEN: 0,
                    BATTLECRUISER: 0
                }
            },
            DARKTEMPLAR: {
                "supply": 2,
                "counters": set([SIEGETANK, BANSHEE]),
                "utility_against":{
                    MARINE: 0,
                    MARAUDER: 0,
                    REAPER: 0,
                    GHOST: 0,
                    HELLION: 0,
                    WIDOWMINE: 0,
                    SIEGETANK: 0,
                    CYCLONE: 0,
                    HELLIONTANK: 0,
                    THOR: 0,
                    VIKING: 0,
                    VIKINGFIGHTER: 0,
                    MEDIVAC: 0,
                    LIBERATOR: 0,
                    BANSHEE: 0,
                    RAVEN: 0,
                    BATTLECRUISER: 0
                }
            },
            ARCHON: {
                "supply": 0,
                "counters": set([]),
                "utility_against":{
                    MARINE: 5,
                    MARAUDER: 5,
                    REAPER: 5,
                    GHOST: 5,
                    HELLION: 5,
                    WIDOWMINE: 5,
                    SIEGETANK: 4,
                    CYCLONE: 5,
                    HELLIONTANK: 5,
                    THOR: 5,
                    VIKING: 9,
                    VIKINGFIGHTER: 8,
                    MEDIVAC: 7,
                    LIBERATOR: 7,
                    BANSHEE: 8,
                    RAVEN: 9,
                    BATTLECRUISER: 7
                }
            },
            IMMORTAL: {
                "supply": 4,
                "counters": set([MARINE, GHOST]),
                "utility_against":{
                    MARINE: 2,
                    MARAUDER: 9,
                    REAPER: 2,
                    GHOST: 3,
                    HELLION: 7,
                    WIDOWMINE: 5,
                    SIEGETANK: 9,
                    CYCLONE: 8,
                    HELLIONTANK: 7,
                    THOR: 8,
                    VIKING: 0,
                    VIKINGFIGHTER: 7,
                    MEDIVAC: 0,
                    LIBERATOR: -8,
                    BANSHEE: -10,
                    RAVEN: -10,
                    BATTLECRUISER: -10
                }
            },
            COLOSSUS: {
                "supply": 6,
                "counters": set([SIEGETANK, VIKING]),
                "utility_against":{
                    MARINE: 9,
                    MARAUDER: 7,
                    REAPER: 9,
                    GHOST: 7,
                    HELLION: 9,
                    WIDOWMINE: 9,
                    SIEGETANK: 6,
                    CYCLONE: 5,
                    HELLIONTANK: 9,
                    THOR: 6,
                    VIKING: -10,
                    VIKINGFIGHTER: 6,
                    MEDIVAC: 0,
                    LIBERATOR: -10,
                    BANSHEE: -10,
                    RAVEN: -10,
                    BATTLECRUISER: -10
                }
            },
            OBSERVER: {
                "supply": 1,
                "counters": set([]),
                "utility_against":{
                    MARINE: 0,
                    MARAUDER: 0,
                    REAPER: 0,
                    GHOST: 0,
                    HELLION: 0,
                    WIDOWMINE: 0,
                    SIEGETANK: 0,
                    CYCLONE: 0,
                    HELLIONTANK: 0,
                    THOR: 0,
                    VIKING: 0,
                    VIKINGFIGHTER: 0,
                    MEDIVAC: 0,
                    LIBERATOR: 0,
                    BANSHEE: 0,
                    RAVEN: 0,
                    BATTLECRUISER: 0
                }
            },
            PHOENIX: {
                "supply": 1,
                "counters": set([]),
                "utility_against":{
                    MARINE: -10,
                    MARAUDER: 0,
                    REAPER: 0,
                    GHOST: -10,
                    HELLION: 0,
                    WIDOWMINE: 0,
                    SIEGETANK: 0,
                    CYCLONE: -7,
                    HELLIONTANK: 0,
                    THOR: -10,
                    VIKING: 5,
                    VIKINGFIGHTER: 0,
                    MEDIVAC: 8,
                    LIBERATOR: 7,
                    BANSHEE: 10,
                    RAVEN: 8,
                    BATTLECRUISER: -2
                }
            },
            VOIDRAY: {
                "supply": 1,
                "counters": set([]),
                "utility_against":{
                    MARINE: -2,
                    MARAUDER: 8,
                    REAPER: 7,
                    GHOST: 5,
                    HELLION: 8,
                    WIDOWMINE: 7,
                    SIEGETANK: 8,
                    CYCLONE: 6,
                    HELLIONTANK: 8,
                    THOR: 5,
                    VIKING: 6,
                    VIKINGFIGHTER: 8,
                    MEDIVAC: 5,
                    LIBERATOR: 5,
                    BANSHEE: 10,
                    RAVEN: 7,
                    BATTLECRUISER: 8
                }
            },
            TEMPEST: {
                "supply": 1,
                "counters": set([]),
                "utility_against":{
                    MARINE: 0,
                    MARAUDER: 0,
                    REAPER: 0,
                    GHOST: 0,
                    HELLION: 0,
                    WIDOWMINE: 0,
                    SIEGETANK: 0,
                    CYCLONE: 0,
                    HELLIONTANK: 0,
                    THOR: 0,
                    VIKING: 0,
                    VIKINGFIGHTER: 0,
                    MEDIVAC: 0,
                    LIBERATOR: 0,
                    BANSHEE: 0,
                    RAVEN: 0,
                    BATTLECRUISER: 0
                }
            },
            CARRIER: {
                "supply": 1,
                "counters": set([]),
                "utility_against":{
                    MARINE: 0,
                    MARAUDER: 0,
                    REAPER: 0,
                    GHOST: 0,
                    HELLION: 0,
                    WIDOWMINE: 0,
                    SIEGETANK: 0,
                    CYCLONE: 0,
                    HELLIONTANK: 0,
                    THOR: 0,
                    VIKING: 0,
                    VIKINGFIGHTER: 0,
                    MEDIVAC: 0,
                    LIBERATOR: 0,
                    BANSHEE: 0,
                    RAVEN: 0,
                    BATTLECRUISER: 0
                }
            }
        }
def terran_units():
    return {
                MARINE: {
                    "counters": set([COLOSSUS]),
                    "supply": 1,
                    "disabled": False
                },
                MARAUDER: {
                    "counters": set([IMMORTAL, VOIDRAY, ZEALOT]),
                    "supply": 2,
                    "disabled": False
                },
                REAPER: {
                    "counters": set([STALKER]),
                    "supply": 1,
                    "disabled": False
                },
                GHOST: {
                    "counters": set([STALKER]),
                    "supply": 2,
                    "disabled": False
                },
                HELLION: {
                    "counters": set([STALKER]),
                    "supply": 2,
                    "disabled": False
                },
                HELLIONTANK: {
                    "supply": 2,
                    "disabled": False
                },
                SIEGETANK: {
                    "counters": set([IMMORTAL, VOIDRAY]),
                    "supply": 3,
                    "disabled": False
                },
                THOR: {
                    "counters": set([IMMORTAL]),
                    "supply": 6,
                    "disabled": False
                },
                BANSHEE: {
                    "counters": set([VOIDRAY]),
                    "supply": 3,
                    "disabled": False
                },
                VIKING: {
                    "counters": set([STALKER]),
                    "supply": 2,
                    "disabled": False
                },
                VIKINGFIGHTER: {
                    "counters": set([STALKER]),
                    "supply": 2,
                    "disabled": False
                },
                RAVEN: {
                    "counters": set([STALKER]),
                    "supply": 2,
                    "disabled": True
                },
                MEDIVAC: {
                    "counters": set([STALKER, VOIDRAY]),
                    "supply": 2,
                    "disabled": False
                },
                BATTLECRUISER: {
                    "counters": set([VOIDRAY]),
                    "supply": 6,
                    "disabled": False
                }
            }
