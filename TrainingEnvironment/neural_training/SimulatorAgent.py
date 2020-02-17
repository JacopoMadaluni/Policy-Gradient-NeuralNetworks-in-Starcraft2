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
        self.HEADLESS = False
        self.terran_units_info = terran_units()

        self.initial_supply = total_army_value
        self.commands = commands

        self.submit_reward = submit_reward


        if not self.commands:
            self.n_zealots   = observation[0]
            self.n_stalkers  = observation[1]
            self.n_immortals = observation[2]

            self.n_marines = observation[3]
            self.n_marauders = observation[4]
            self.n_tanks = observation[5]
            self.n_banshees = observation[6]


    async def on_start_async(self):
        if self.commands:
            for command in self.commands:
                await self.chat_send(command)
        else:
            await self.chat_send("let us begin!")
            await self.chat_send("-marine {}".format(self.n_marines))
            await self.chat_send("-marauder {}".format(self.n_marauders))
            await self.chat_send("-stank {}".format(self.n_tanks))
            await self.chat_send("-banshee {}".format(self.n_banshees))


            await self.chat_send("-zealot {}".format(self.n_zealots))
            await self.chat_send("-stalker {}".format(self.n_stalkers))
            await self.chat_send("-immortal {}".format(self.n_immortals))
        await self.chat_send("-begin")


    async def on_step(self, iteration):
        self.compute_enemy_supply_belief()

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
            reward = self.normalize_supply_left(self.supply_army)
            self.submit_reward(reward)

        else:
            # How much army does enemy have left
            enemy_supply = self.compute_enemy_supply_belief()
            if self.supply_army > enemy_supply:
                # Timed out, did not actually lose
                reward = self.normalize_supply_left(self.supply_army)
                self.submit_reward(reward)
            else:    
                reward = (-1) * self.normalize_supply_left(enemy_supply)
                self.submit_reward(reward)
