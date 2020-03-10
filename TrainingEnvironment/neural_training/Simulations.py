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
from evaluator import army_generator
from info import *

terran_units  = terran_units()
protoss_units = protoss_units()
all_units     = all_units()


class Simulation:

    def __init__(self):
        pass

    def on_end(self, result):
        print("ON END CALLED WITH: {}".format(result))
        self.result = result

    def simulate_exchange(self):
        result = run_game(maps.get("TrainingEnvironment"),
            [Bot(Race.Protoss, SimulatorAgent(self.current_observation, self.total_supply, self.commands, self.on_end)), Computer(Race.Terran, Difficulty.Easy)],
            realtime=False)
        print("Result in sim {}".format(self.result))
        return self.result


class SimpleSimulation():

    def __init__(self):
        # generating army
        self.n_marauders = 0
        self.n_hellbats  = 0
        self.n_banshees  = 0
        self.commands = []

        self.normalize = True
        self.use_model_rewards = True

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

        self.model_input = None
        self.init_model()

        self.model = model.ArmyCompModel(self.model_input)
        self.current_supply = 0
        self.ready = False

    def init_model(self):
        self.model_input = []
        if self.n_marauders != 0:
            self.model_input.append([MARAUDER, self.n_marauders])
        if self.n_hellbats != 0:
            self.model_input.append([HELLIONTANK, self.n_hellbats])
        if self.n_banshees != 0:
            self.model_input.append([BANSHEE, self.n_banshees])


    def disable_normalization(self):
        self.normalize = False

    def initialize_in_game_simulation_commands(self):
        for u, n in zip(self.unit_namespace, self.current_observation):
            self.commands.append("-{} {}".format(u, n))
        print("Initialized commands: {}".format(self.commands))

    def normalize_observation(self):
        o = self.current_observation
        total_ally_supply = o[0]*2 + o[1]*2 + o[2]*2 + o[3]
        if total_ally_supply == 0:
            total_ally_supply = 1
        normalized_obs = []
        normalized_obs.append(o[0]*2/total_ally_supply)
        normalized_obs.append(o[1]*2/total_ally_supply)
        normalized_obs.append(o[2]*2/total_ally_supply)
        normalized_obs.append(o[3]/total_ally_supply)

        normalized_obs.append(o[4]*2/self.total_supply)
        normalized_obs.append(o[5]*2/self.total_supply)
        normalized_obs.append(o[6]*3/self.total_supply)
        print("Normalized observation: {}".format(normalized_obs))
        return normalized_obs

    def get_current_observation(self):
        if self.normalize:
            normalized = self.normalize_observation()
            return np.array(normalized)
        else:
            return np.array(self.current_observation)

    def get_raw_observation(self):
        return self.current_observation

    def add_unit(self, unit):
        print("Action arrived: {}".format(unit))
        reward = 0
        if unit == 0:
            self.n_zealots += 1
            self.current_supply += 2
            self.current_observation[0] += 1
            reward = self.model.utility_of(ZEALOT) * 0.1
        elif unit == 1:
            self.n_stalkers += 1
            self.current_supply += 2
            self.current_observation[1] += 1
            reward = self.model.utility_of(STALKER) * 0.1
        elif unit == 2:
            self.n_phoenixes += 1
            self.current_supply += 2
            self.current_observation[2] += 1
            reward = self.model.utility_of(PHOENIX) * 0.1
        elif unit == 3:
            self.n_probes += 1
            self.current_supply += 1
            self.current_observation[3] += 1
            reward = self.model.utility_of(PROBE) * 0.1
        else:
            print("####### NO ACTION CHOSE")
        if self.current_supply >= self.total_supply:
                self.initialize_in_game_simulation_commands()
                self.ready = True

        #observation_, reward, done, info
        return self.get_current_observation(), reward, self.ready, ""

    def on_end(self, result):
        self.result = result


    def simulate_exchange(self):
        result = run_game(maps.get("TrainingEnvironment"),
            [Bot(Race.Protoss, SimulatorAgent(self.current_observation, self.total_supply, self.commands, self.on_end)), Computer(Race.Terran, Difficulty.Easy)],
            realtime=False)

        return self.result


class HardSimulation(Simulation):

    def __init__(self, initial_namespace):
        super(HardSimulation, self).__init__()

        self.use_model_rewards = True
        self.use_supply_in_obs = True

         # generating army
        self.commands  = []
        self.normalize = True

        rand = random.uniform(0,6)
        self.army = None
        if rand <= 1:
            self.army = army_generator.small_random_army()
            print(">>>> Small random army")
        elif rand <= 2:
            self.army = army_generator.medium_random_army()
            print(">>>> Medium random army")
        elif rand <= 3:
            self.army = army_generator.big_random_army()
            print(">>>> Big random army")
        elif rand <=4:
           self.army = army_generator.mech_army(random.choice([40, 45, 50, 55, 60, 65, 70]))
           print(">>>> Mech army")
        else:
            self.army = army_generator.bio_army(random.randint(22,70))
            print(">>>> Bio army")


        self.n_of_ally_different_units = len(initial_namespace)
        self.unit_namespace = list(initial_namespace)


        # Order matters
        self.e_unit_namespace = [k for k in terran_units if terran_units[k]["disabled"] == False]
        self.unit_namespace += self.e_unit_namespace
        print("Initialized name space: {}".format(self.unit_namespace))


        self.current_observation = [0 for _ in self.unit_namespace]
        self.init_observation()
        print("Initial observation: {}".format(self.current_observation))

        self.total_supply = sum(terran_units[unit[0]]["supply"]*unit[1] for unit in self.army)
        print("Enemy supply: {}".format(self.total_supply))

        self.model = model.ArmyCompModel(self.army)
        self.current_supply = 0
        self.ready = False

    def init_observation(self):
        for e in self.army:
            for i, u_type in enumerate(self.e_unit_namespace):
                if u_type == e[0]:
                    index = i + self.n_of_ally_different_units
                    assert self.current_observation[index] == 0
                    self.current_observation[index] = e[1]


    def disable_normalization(self):
        self.normalize = False

    def disable_model_rewards(self):
        self.use_model_rewards = False

    def disable_total_supply_obs(self):
        self.use_supply_in_obs = False



    def initialize_in_game_simulation_commands(self):
        for u_type, amount in zip(self.unit_namespace, self.current_observation):
            self.commands.append("-{} {}".format(all_units[u_type]["name"], amount))

        print("Initialized commands: {}".format(self.commands))

    def normalize_observation(self):
        o = self.current_observation
        total_ally_supply = sum([protoss_units[self.unit_namespace[i]]["supply"]*self.current_observation[i] for i in range(self.n_of_ally_different_units)])
        if total_ally_supply == 0:
            total_ally_supply = 1
        normalized_obs = []
        for i in range(self.n_of_ally_different_units):
            unit_type = self.unit_namespace[i]
            normalized_obs.append(o[i]*protoss_units[unit_type]["supply"]/total_ally_supply)
        for i in range(self.n_of_ally_different_units, len(self.current_observation)):
            unit_type = self.unit_namespace[i]
            normalized_obs.append(o[i]*terran_units[unit_type]["supply"]/self.total_supply)

        if self.use_supply_in_obs:
            normalized_obs = [self.total_supply - self.current_supply] + normalized_obs
        print("Normalized observation: {}".format(normalized_obs))
        return normalized_obs


    def get_current_observation(self):
        if self.normalize:
            normalized = self.normalize_observation()
            return np.array(normalized)
        else:
            return np.array([self.total_supply - self.current_supply] + self.current_observation)

    def get_raw_observation(self):
        return self.current_observation

    def add_unit(self, unit):
        unit_type = self.unit_namespace[unit]
        self.current_observation[unit] += 1
        self.current_supply += protoss_units[unit_type]["supply"]

        reward = 0
        if self.use_model_rewards:
            reward = self.model.utility_of(unit_type) * 10

        if self.current_supply >= self.total_supply:
            self.initialize_in_game_simulation_commands()
            self.ready = True

        #observation_, reward, done, info
        return self.get_current_observation(), reward, self.ready, ""
