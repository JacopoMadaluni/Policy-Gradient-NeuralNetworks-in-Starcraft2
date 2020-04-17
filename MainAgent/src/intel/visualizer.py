import numpy as np
import cv2
from ..utils.constants      import *
from ..utils.units          import getUnits
from ..utils.function_utils import agent_method


class Visualizer:
    """
    The Visualizer helps visualize the state of the game while running headless.
    It is only possible to run a headless version of the game on linux.
    """
    def __init__(self):
        self.GREEN           = (0, 255, 0)
        self.units_info      = getUnits()
        self.visual_data     = None
        self.bad_areas       = []

    @agent_method
    def draw_mineral_fields(self, agent=None):    
        """
        Draws all the mineral fields as light blue dots.
        """
        for field in agent.state.mineral_field:
            pos = field.position
            cv2.circle(self.game_data, (int(pos[0]), int(pos[1])), 1, (255, 255,65 ), -1)

    @agent_method
    def draw_information(self, agent=None):
        """
        Draws all units and structures that the agent sees.
        """
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
        """
        Draws in blue the areas where the agent cannot build.
        """
        for area in self.bad_areas:
            for pos in area:
                cv2.circle(self.game_data, (int(pos[0]), int(pos[1])), 2, (255, 0, 0), -1)       

    def set_bad_areas(self, bad_areas):
        self.bad_areas = bad_areas

    @agent_method
    def print_info_to_console(self, agent=None):
        pass

