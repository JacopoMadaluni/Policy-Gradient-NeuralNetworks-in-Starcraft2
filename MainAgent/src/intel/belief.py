
from ..utils.constants import *
from ..utils.function_utils import agent_method
from TrainingEnvironment.info import terran_units

import random

class Belief:

    def __init__(self):
        self.enemy_total_supply = 0
        self.enemy_army_comp = None
        self.exclude = [SCV, MULE, RAVEN]
        self.initialize_enemy_army_namespace()
        
        print("Initialized belief: {}".format(self.enemy_army_comp))

    def initialize_enemy_army_namespace(self):
        army_namespace = {}
        all_units_info = terran_units()
        for k in all_units_info:
            unit_info = all_units_info[k]
            if not unit_info["disabled"]:
                army_namespace[k] = 0

        self.enemy_army_comp = army_namespace        


    @agent_method
    def update(self, agent=None):
        structures = agent.known_enemy_structures
        
        units = list(filter(lambda unit: unit.type_id not in self.exclude, agent.known_enemy_units - structures))

        if len(units) > 0:
            for u in units:
                typ = u.type_id
                if typ in self.enemy_army_comp:
                    self.enemy_army_comp[typ] += 1



    def get_normalized_belief(self):
        normalized_bel = self.enemy_army_comp.copy()
        total = sum(normalized_bel[k] for k in normalized_bel)
        if total == 0:
            total = 1
        for k in normalized_bel:
            normalized_bel[k] = normalized_bel[k]/total

        return normalized_bel

    def get_normalized_belief_as_array(self):
        normalized_bel = self.get_normalized_belief()
        return [normalized_bel[k] for k in normalized_bel]      

