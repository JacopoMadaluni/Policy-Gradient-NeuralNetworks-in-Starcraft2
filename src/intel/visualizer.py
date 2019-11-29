import numpy as np
import cv2
from ..utils.constants      import *
from ..utils.units          import getUnits
from ..utils.function_utils import agent_method


class Visualizer:


    def __init__(self):
        self.GREEN           = (0, 255, 0)
        self.units_info      = getUnits()
        self.visual_data     = None
        self.military_weight = 0

    @agent_method
    def compute_military_weight(self, agent=None):
        total_weight = 0
        #print(dir(self.agent.units))
        for UNIT in self.units_info.protossUnits:
            u_info = self.units_info.protossUnits[UNIT]
            if UNIT == PROBE or u_info["type"] == "structure":
                # ignore probes and structures
                continue
            amount = len(agent.units(UNIT))
            weight = u_info["supply"]
            total_weight += weight*amount
        return total_weight    

    @agent_method
    def draw_resources(self, agent=None):

        line_max = 50
        mineral_ratio = agent.minerals / 2500
        if mineral_ratio > 1.0:
            mineral_ratio = 1.0


        vespene_ratio = agent.vespene / 2500
        if vespene_ratio > 1.0:
            vespene_ratio = 1.0

        population_ratio = agent.supply_left / agent.supply_cap
        if population_ratio > 1.0:
            population_ratio = 1.0

        plausible_supply = agent.supply_cap / 200.0

        military_weight = self.compute_military_weight() / (agent.supply_cap-agent.supply_left)
        self.military_weight = military_weight
        if military_weight > 1.0:
            military_weight = 1.0


        cv2.line(self.game_data, (0, 19), (int(line_max*military_weight), 19),  (250, 250, 200), 3)  # army/supply ratio ?????????
        cv2.line(self.game_data, (0, 15), (int(line_max*plausible_supply), 15), (220, 200, 200), 3)  # plausible supply (supply/200.0)
        cv2.line(self.game_data, (0, 11), (int(line_max*population_ratio), 11), (150, 150, 150), 3)  # population ratio (supply_left/supply)
        cv2.line(self.game_data, (0, 7),  (int(line_max*mineral_ratio), 7),     (210, 200, 0), 3)         # gas / 2500
        cv2.line(self.game_data, (0, 3),  (int(line_max*vespene_ratio), 3),     (0, 255, 25), 3)          # minerals (minerals/2500)    

    @agent_method
    def draw_information(self, agent=None):
        map_size = agent.game_info.map_size
        self.game_data = np.zeros((map_size[1], map_size[0], 3), np.uint8)

        # UNIT: [SIZE, (BGR COLOR)]
        draw_dict = {
                     NEXUS: [15, (0, 255, 0)],
                     PYLON: [3, (20, 235, 0)],
                     PROBE: [1, (55, 200, 0)],
                     
                     IMMORTAL: [2, (55, 250, 0)],
                     STALKER: [1, (55, 230, 0)],
                     

                     ASSIMILATOR: [2, (55, 200, 0)],
                     GATEWAY: [3, (200, 100, 0)],
                     CYBERNETICSCORE: [3, (150, 150, 0)],
                     STARGATE: [5, (255, 0, 0)],
                     ROBOTICSFACILITY: [5, (215, 155, 0)],

                     VOIDRAY: [3, (255, 100, 0)],
                    }

        for unit_type in draw_dict:
            for unit in agent.units(unit_type).ready:
                pos = unit.position
                cv2.circle(self.game_data, (int(pos[0]), int(pos[1])), draw_dict[unit_type][0], draw_dict[unit_type][1], -1)



        main_base_names = ["nexus", "commandcenter", "hatchery"]
        for enemy_building in agent.known_enemy_structures:
            pos = enemy_building.position
            if enemy_building.name.lower() not in main_base_names:
                cv2.circle(self.game_data, (int(pos[0]), int(pos[1])), 5, (200, 50, 212), -1)
        for enemy_building in agent.known_enemy_structures:
            pos = enemy_building.position
            if enemy_building.name.lower() in main_base_names:
                cv2.circle(self.game_data, (int(pos[0]), int(pos[1])), 15, (0, 0, 255), -1)

        for enemy_unit in agent.known_enemy_units:

            if not enemy_unit.is_structure:
                worker_names = ["probe",
                                "scv",
                                "drone"]
                # if that unit is a PROBE, SCV, or DRONE... it's a worker
                pos = enemy_unit.position
                if enemy_unit.name.lower() in worker_names:
                    cv2.circle(self.game_data, (int(pos[0]), int(pos[1])), 1, (55, 0, 155), -1)
                else:
                    cv2.circle(self.game_data, (int(pos[0]), int(pos[1])), 3, (50, 0, 215), -1)

        for obs in agent.units(OBSERVER).ready:
            pos = obs.position
            cv2.circle(self.game_data, (int(pos[0]), int(pos[1])), 1, (255, 255, 255), -1)

        self.draw_resources()

        # flip horizontally to make our final fix in visual representation:
        self.visual_data = cv2.flip(self.game_data, 0)

        if not agent.HEADLESS:
            resized = cv2.resize(self.visual_data, dsize=None, fx=2, fy=2)

            cv2.imshow('Intel', resized)
            cv2.waitKey(1)



#if __name__ == "__main__":
    #v = Visualizer(None)        