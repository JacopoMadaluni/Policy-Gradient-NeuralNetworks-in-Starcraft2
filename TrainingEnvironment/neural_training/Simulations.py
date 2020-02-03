import sc2
import random
import time
import numpy as np
import math
import matplotlib.pyplot as plt 
import time
from sc2 import run_game, maps, Race, Difficulty, position, Result
from sc2.player import Bot, Computer
from .SimulatorAgent import SimulatorAgent
from mathematical_model import model


class SimpleSimulation():

    def __init__(self):
        # generating army
        self.n_marauders = 0
        self.n_hellbats  = 0
        self.n_banshees  = 0
        self.commands = []

        rand = random.uniform(0,4)
        if rand <= 1:
            self.n_marauders = round(random.uniform(1, 20))
        elif rand <= 2:
            self.n_hellbats  = round(random.uniform(2, 10))
        elif rand <= 3:
            self.n_banshees  = round(random.uniform(1, 10))
        else:
            self.n_marauders = round(random.uniform(1, 20))         

        self.n_zealots    = 0
        self.n_stalkers   = 0
        self.n_phoenixes  = 0
        self.n_probes     = 0

        self.unit_namespace = ["zealot", "stalker", "phoenix", "probe", "marauder", "hellbat", "banshee"]
        self.current_observation = [0, 0, 0, 0, self.n_marauders, self.n_hellbats, self.n_banshees]


        self.total_supply = self.n_marauders * 2 + self.n_hellbats * 2 + self.n_banshees * 3
        print("Enemy supply: {}".format(self.total_supply))
        self.current_supply = 0
        self.ready = False
  

    def initialize_in_game_simulation_commands(self):
        for u, n in zip(self.unit_namespace, self.current_observation):
            self.commands.append("-{} {}".format(u, n))
        print("Initialized commands: {}".format(self.commands))    

    def get_current_observation(self):
        return np.array(self.current_observation)

    def add_unit(self, unit):
        if unit == 0:
            self.n_zealots += 1
            self.current_supply += 2
            self.current_observation[0] += 1    
        elif unit == 1:
            self.n_stalkers += 1
            self.current_supply += 2
            self.current_observation[1] += 1 
        elif unit == 3:
            self.n_phoenixes += 1
            self.current_supply += 2
            self.current_observation[2] += 1    
        else:
            self.n_probes += 1
            self.current_supply += 1
            self.current_observation[3] += 1 
        if self.current_supply >= self.total_supply:
                self.initialize_in_game_simulation_commands()
                self.ready = True    

        #observation_, reward, done, info         
        return self.get_current_observation(), 0, self.ready, ""    

    def on_end(self, result):
        self.result = result        


    def simulate_exchange(self):
        result = run_game(maps.get("TrainingEnvironment"),
            [Bot(Race.Protoss, SimulatorAgent(self.current_observation, self.total_supply, self.commands, self.on_end)), Computer(Race.Terran, Difficulty.Easy)],
            realtime=False)   

        #if result == Result.Victory:
        #    return 1
        #else:
        #    return -1
        return self.result

