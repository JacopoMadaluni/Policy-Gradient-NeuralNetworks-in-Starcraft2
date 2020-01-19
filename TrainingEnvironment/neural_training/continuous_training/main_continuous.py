import tensorflow as tf
from tensorflow import keras
import sc2
import random
import time
import numpy as np
import math
import matplotlib.pyplot as plt 
import threading
from sc2 import run_game, maps, Race, Difficulty, position, Result
from sc2.player import Bot, Computer
from PolicyGradient import PolicyGradientAgent
from Simulations import SimpleSimulation

from socketIO_client import SocketIO, LoggingNamespace
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class Exchange:

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

            self.result = None

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
    
    def initialize_in_game_simulation_commands(self):
        for u, n in zip(self.unit_namespace, self.current_observation):
            self.commands.append("-{} {}".format(u, n))
        print("Initialized commands: {}".format(self.commands))         

    def get_current_observation(self):
        return np.array(self.current_observation)        


def plotLearning(scores, filename, x=None, window=5):   
    N = len(scores)
    running_avg = np.empty(N)
    for t in range(N):
	    running_avg[t] = np.mean(scores[max(0, t-window):(t+1)])
    if x is None:
        x = [i for i in range(N)]
    plt.ylabel('Score')       
    plt.xlabel('Game')                     
    plt.plot(x, running_avg)
    plt.savefig(filename)

class Main:

    def __init__(self, num_episodes):
        self.socket = SocketIO('localhost', 3000, LoggingNamespace)
        self.socket.on("result", self.on_result)     

        self.iteration = 0
        self.score_history = []
        self.num_episodes = num_episodes

        self.agent = PolicyGradientAgent(ALPHA=0.0005, input_dims=7, GAMMA=0.99,
                                n_actions=4, layer1_size=64, layer2_size=64,
                                chkpt_dir='tmp/')
                     
        #agent.load_checkpoint()


    def on_result(self,result):
        print("result: {}".format(result))

        self.score_history.append(result)
        self.agent.learn()  
        self.agent.save_checkpoint() 
        self.iteration += 1

        if self.iteration > self.num_episodes:
            filename = 'last_run.png'
            plotLearning(self.score_history, filename=filename, window=25)
        else:
            self.next_exchange()  


    def next_exchange(self):
        exchange = Exchange()
        observation = exchange.get_current_observation()
        done = False
        while not done:
            action = self.agent.choose_action(observation)
            print(action)
            observation_, reward, done, info = exchange.add_unit(action)
            self.agent.store_transition(observation, action, reward)
            observation = observation_

        #score = simulation.simulate_exchange()   
        self.socket.emit("new_simulation", exchange.commands, exchange.total_supply)
        self.socket.wait() 

          

if __name__ == "__main__":
    main = Main(50)
    main.next_exchange()