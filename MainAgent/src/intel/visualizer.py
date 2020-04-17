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
        self.bad_areas       = []

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
    def draw_mineral_fields(self, agent=None):    
        for field in agent.state.mineral_field:
            pos = field.position
            cv2.circle(self.game_data, (int(pos[0]), int(pos[1])), 1, (255, 255,65 ), -1)

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

        

        for unit_type in self.units_info.protoss_drawing_order:
            visualization = self.units_info.protossUnits[unit_type]["visualization"]
            color = visualization["color"]
            size  = visualization["size"]
            for unit in agent.units(unit_type).ready:
                pos = unit.position
                cv2.circle(self.game_data, (int(pos[0]), int(pos[1])), size, color, -1)

        

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
            if enemy_unit.is_structure:
                continue
            unit_type = enemy_unit.type_id
            if unit_type in self.units_info.terran_units:
                pos = enemy_unit.position
                visualization = self.units_info.terran_units[unit_type]["visualization"]
                color = visualization["color"]
                size  = visualization["size"]
                cv2.circle(self.game_data, (int(pos[0]), int(pos[1])), size, color, -1)

        self.draw_mineral_fields()    
        self.draw_bad_areas()

        # flip horizontally to make our final fix in visual representation:
        self.visual_data = cv2.flip(self.game_data, 0)

        if not agent.HEADLESS:
            resized = cv2.resize(self.visual_data, dsize=None, fx=2, fy=2)

            cv2.imshow('Visual Data', resized)
            cv2.waitKey(1)

    def draw_bad_areas(self):
        for area in self.bad_areas:
            for pos in area:
                cv2.circle(self.game_data, (int(pos[0]), int(pos[1])), 2, (255, 0, 0), -1)       


    def set_bad_areas(self, bad_areas):
        self.bad_areas = bad_areas

    @agent_method
    def print_info_to_console(self, agent=None):
        pass



#if __name__ == "__main__":
    #v = Visualizer(None)        