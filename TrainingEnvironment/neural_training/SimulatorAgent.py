# 165 iterations per minute

import sc2
import random
import time
import numpy as np
import math
import matplotlib.pyplot as plt
import threading
from sc2 import run_game, maps, Race, Difficulty, position, Result
from sc2.player import Bot, Computer
from info import terran_units


class SimulatorAgent(sc2.BotAI):


    def __init__(self, observation, total_army_value, commands, submit_reward):
        self.ITERATIONS_PER_MINUTE = 165
        self.terran_units_info = terran_units()

        self.initial_supply = total_army_value
        self.commands = commands

        self.submit_reward = submit_reward

    async def on_start_async(self):
        if self.commands:
            for command in self.commands:
                await self.chat_send(command)
        await self.chat_send("-begin")


    async def on_step(self, iteration):
        pass

    def normalize_supply_left(self, leftover):
        return leftover/self.initial_supply

    def compute_enemy_supply_belief(self):
        enemy_leftover_supply = 0
        for unit in self.known_enemy_units:
            u_type = unit.type_id
            enemy_leftover_supply += self.terran_units_info[u_type]["supply"]
        return enemy_leftover_supply


    def on_end(self, result):
        print("Game ended")
        print("Result: {}".format(result))
        if result == Result.Victory:
            # How much army do I have left
            reward = 500 
            self.submit_reward(reward)

        else:
            # How much army does enemy have left
            enemy_supply = self.compute_enemy_supply_belief()
            reward = (-500) 
            self.submit_reward(reward)
