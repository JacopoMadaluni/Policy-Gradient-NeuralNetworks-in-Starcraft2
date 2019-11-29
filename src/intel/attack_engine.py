import random
import numpy as np

from ..utils.constants      import *
from ..utils.units          import getUnits
from ..utils.function_utils import agent_method
class Attacker:

    def __init__(self, visualizer, trainer):
        self.visualizer = visualizer
        self.trainer    = trainer
        self.units_info = getUnits()

        self.next_iteration_attack = 0

        

    @agent_method
    async def attack_with_model(self, agent=None):

        if self.visualizer.military_weight > 0:
            choice = random.randrange(0, 4)
            target = False
            if agent.iteration > self.next_iteration_attack:
                if choice == 0:
                    # no attack
                    wait = random.randrange(20, 165)
                    self.next_iteration_attack = agent.iteration + wait
                    

                elif choice == 1:
                    #attack_unit_closest_nexus
                    if len(agent.known_enemy_units) > 0:
                        target = agent.known_enemy_units.closest_to(random.choice(agent.units(NEXUS)))

                elif choice == 2:
                    #attack enemy structures
                    if len(agent.known_enemy_structures) > 0:
                        target = random.choice(agent.known_enemy_structures)

                elif choice == 3:
                    #attack_enemy_start
                    target = agent.enemy_start_locations[0]

                if target:
                    for UNIT in self.units_info.protossUnits:
                        u_info = self.units_info.protossUnits[UNIT]
                        if UNIT != PROBE and u_info["type"] == "unit":
                            for u in agent.units(UNIT):
                                await agent.do(u.attack(target))
                y = np.zeros(4)
                y[choice] = 1
                self.trainer.add_attack_data_snapshot(self.visualizer.visual_data, y)