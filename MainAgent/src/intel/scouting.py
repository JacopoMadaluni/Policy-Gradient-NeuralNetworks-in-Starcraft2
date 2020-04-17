import random
import numpy as np

from sc2 import position

from ..utils.constants      import *
from ..utils.units          import getUnits
from ..utils.function_utils import agent_method


class Scouter:


    def __init__(self):
        self.variances      = PositionVariances()    
        self.map_scout      = None
        self.next_scout_iteration = 0

    @agent_method
    def choose_map_scout(self, agent=None):
        if self.map_scout is None:
            if agent.units(STALKER).exists:
                stalker = random.choice(agent.units(STALKER))
                self.map_scout = stalker
            else:
                self.map_scout = random.choice(agent.units(PROBE))
        elif self.map_scout == PROBE:
            if agent.units(STALKER).exists:
                stalker = random.choice(agent.units(STALKER))
                self.map_scout = stalker
            else:
                return
        return None            

    @agent_method
    def update_next_iteration(self, agent=None):
        delay = random.randrange(20, 165)
        self.next_scout_iteration = agent.iteration + delay

    @agent_method
    async def scout_enemy_base(self, unit, agent=None):
        enemy_location = agent.enemy_start_locations[0]
        position = self.variances.random_enemy_start_location_variance(agent.game_info.map_size, enemy_location)
        await agent.do(unit.move(position))

    @agent_method
    async def scout_map(self, agent=None):
        if agent.iteration > self.next_scout_iteration:
            self.choose_map_scout()
            if self.map_scout is not None:
                print("redirecting scout")    
                position = self.variances.random_position_in_map(agent.game_info.map_size)
                self.update_next_iteration()
                await agent.do(self.map_scout.move(position))


class PositionVariances:

    def position_of(self, x, y):
        return position.Point2(position.Pointlike((x, y)))

    def random_enemy_start_location_variance(self, map_size, enemy_start_location):
        return self.position_variance(map_size, enemy_start_location) 

    def position_variance(self, map_size, position):
        x = position[0]
        y = position[1]

        x += ((random.randrange(-20, 20))/100) * position[0]
        y += ((random.randrange(-20, 20))/100) * position[1]

        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > map_size[0]:
            x = map_size[0]
        if y > map_size[1]:
            y = map_size[1]

        target = self.position_of(x, y)
        return target       

    def random_position_in_map(self, map_size):
        x = random.randrange(map_size[0])
        y = random.randrange(map_size[1])
        
        return self.position_of(x, y)
