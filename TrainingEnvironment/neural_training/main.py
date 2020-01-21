import tensorflow as tf
from tensorflow import keras
import sc2
import random
import time
import numpy as np
import math
import matplotlib.pyplot as plt
import threading
import os
from sc2 import run_game, maps, Race, Difficulty, position, Result
from sc2.player import Bot, Computer
from PolicyGradient import PolicyGradientAgent
from Simulations import SimpleSimulation







class Simulation():

    def __init__(self):
        # generating army
        self.n_marines   = round(random.uniform(0, 10))
        self.n_marauders = round(random.uniform(0, 10))
        self.n_tanks     = round(random.uniform(0, 5))
        self.n_banshees  = round(random.uniform(0, 5))

        self.n_zealots   = 0
        self.n_stalkers  = 0
        self.n_immortals = 0

        self.current_observation = [0, 0, 0, self.n_marines, self.n_marauders, self.n_tanks, self.n_banshees]


        self.total_supply = self.n_marines + self.n_marauders * 2 + self.n_tanks * 3 + self.n_banshees * 3
        print("Enemy supply: {}".format(self.total_supply))
        self.current_supply = 0
        self.ready = False

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
        else:
            self.n_immortals += 1
            self.current_supply += 4
            self.current_observation[2] += 1
        if self.current_supply >= self.total_supply:
                self.ready = True

        #observation_, reward, done, info
        return self.get_current_observation(), 0, self.ready, ""


    def simulate_exchange(self):
        result = run_game(maps.get("TrainingEnvironment"),
            [Bot(Race.Protoss, SimulatorAgent(self.current_observation)), Computer(Race.Terran, Difficulty.Easy)],
            realtime=True)
        if result == Result.Victory:
            return 1
        else:
            return -1


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


def get_user_inputs(checkpoints_dir):
    simulation_location = input("Choose save location \n> ")
    load_checkpoint = False
    full_dir_location = os.path.join(os.path.abspath(os.getcwd()), checkpoints_dir, simulation_location)
    if os.path.exists(full_dir_location):
        if input("Do you want to load the previous checkpoint for this simulation? [y/n]\n> ") == "y":
            load_checkpoint = True
    return simulation_location, load_checkpoint

def save_info(agent, win_loss, save_dir):
    win_ratio = (win_loss[0]/(win_loss[0]+win_loss[1]))
    with open(os.path.join(save_dir, "info"), "w+") as f:
        f.write("{}\nWin ratio: {}".format(repr(agent), win_ratio))

    graphname = os.path.join(save_dir, 'graph.png')
    plotLearning(score_history, filename=graphname, window=25)

if __name__ == "__main__":
    checkpoints_dir = "checkpoints/"
    simulation_location, load_checkpoint = get_user_inputs(checkpoints_dir)
    simulation_dir = os.path.join(checkpoints_dir, simulation_location)



    agent = PolicyGradientAgent(ALPHA=0.0005, input_dims=7, GAMMA=0.99,
                                n_actions=4, layer1_size=49, layer2_size=49,
                                chkpt_dir=simulation_dir)

    if load_checkpoint:
        agent.load_checkpoint()
        print("Checkpoint successfully loaded")

    score_history = []
    win_loss = [0, 0]
    score = 0
    num_episodes = 10

    for i in range(num_episodes):
        print('episode: ', i,'score: ', score)
        done = False
        score = 0
        simulation = SimpleSimulation()
        observation = simulation.get_current_observation()
        while not done:
            action = agent.choose_action(observation)
            print(action)
            observation_, reward, done, info = simulation.add_unit(action)
            agent.store_transition(observation, action, reward)
            observation = observation_
            score += reward

        score += simulation.simulate_exchange()

        # Keep track of win/loss ratio
        if score > 0:
            win_loss[0] += 1
        else:
            win_loss[1] += 1

        print("Result: {}".format(score))
        agent.finish_transition_group(score)
        score_history.append(score)
        agent.learn()

        agent.save_checkpoint()

    save_info(agent, win_loss, simulation_dir)
