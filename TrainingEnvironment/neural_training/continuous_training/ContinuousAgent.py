
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
from flask import Flask
from flask_socketio import SocketIO, emit
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


class ContinuousSimulatorAgent(sc2.BotAI):
    
    def __init__(self):
        self._init_socket()
        self.setting_commands = False
        self.next_commands = []
        self.total_supply = 0
        self.simulation_is_running = False
        self.terran_units_info = terran_units()

        self.beginning_time = 0

    def _init_socket(self):
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'secret!'
        socketio = SocketIO(app) 
        

        @socketio.on("connect")
        def connect():
            print("Neural Network connected")
        @socketio.on("new_simulation")
        def new_simulation(commands, total_army_supply):
            print("On new simulation")
            self.next_commands = commands
            self.total_supply  = total_army_supply

        self.socket = socketio
        self.app    = app
        threading.Thread(target=self._run_socket_listener).start()

    def _run_socket_listener(self):
        self.socket.run(self.app, port=3000)


    async def start_new_exchange(self):
        for command in self.next_commands:
            await self.chat_send(command)
        self.next_commands = []    
        await self.chat_send("-begin")
        self.simulation_is_running = True 
        print("end start_new_exchange, supply: {}".format(self.supply_army))   

    def normalize_supply_left(self, leftover):
        return leftover/self.total_supply

    def compute_enemy_supply_belief(self):
        enemy_leftover_supply = 0
        for unit in self.known_enemy_units:
            u_type = unit.type_id
            enemy_leftover_supply += self.terran_units_info[u_type]["supply"]
        return enemy_leftover_supply    

    # 165 iterations per minute
    async def on_step(self, iteration):
        if len(self.next_commands) > 0:
            await self.start_new_exchange()
            self.beginning_time = self.time
            return

        if self.simulation_is_running:
            current_enemy_supply = self.compute_enemy_supply_belief()
            current_ally_supply  = self.supply_army 

            print("{}, {}".format(self.time, self.beginning_time))
            if (current_ally_supply == 0 and current_enemy_supply ==0):
                # Bug, that's not a good way to fix this
                return
            if (current_ally_supply == 0 or self.time - self.beginning_time > 60):
                # Lose, emit result
                reward = (-1) * self.normalize_supply_left(current_enemy_supply)
                self.simulation_is_running = False
                await self.chat_send("-reset")
                self.socket.emit("result", reward)
            elif (current_enemy_supply == 0):    
                # Win, emit result
                reward = self.normalize_supply_left(self.supply_army)               
                self.simulation_is_running = False
                await self.chat_send("-reset")
                self.socket.emit("result", reward)

                #or iteration - self.beginning_iteration > 165