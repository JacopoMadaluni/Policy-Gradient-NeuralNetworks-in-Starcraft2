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
from PolicyGradient_old import PolicyGradientAgent
from Simulations import SimpleSimulation

def get_user_inputs(checkpoints_dir):
    simulation_location = input("Choose model location \n> ")
    episodes = int(input("How many episodes? \n>"))
    load_checkpoint = False
    full_dir_location = os.path.join(os.path.abspath(os.getcwd()), checkpoints_dir, simulation_location)

    return simulation_location, episodes

def save_info(agent, win_loss, save_dir):
    win_ratio = (win_loss[0]/(win_loss[0]+win_loss[1]))
    with open(os.path.join(save_dir, "info"), "w+") as f:
        f.write("{}\nWin ratio: {}".format(repr(agent), win_ratio))

    graphname = os.path.join(save_dir, 'graph.png')
    plotLearning(score_history, filename=graphname, window=25)

if __name__ == "__main__":
    checkpoints_dir = "checkpoints/"
    simulation_location, num_episodes = get_user_inputs(checkpoints_dir)
    simulation_dir = os.path.join(checkpoints_dir, simulation_location)



    agent = PolicyGradientAgent(ALPHA=0.0005, input_dims=7, GAMMA=0.99,
                                n_actions=4, layer1_size=49, layer2_size=49,
                                chkpt_dir=simulation_dir)


    agent.load_checkpoint()
    print("Checkpoint successfully loaded")

    score = 0
    observations = []

    for i in range(num_episodes):
        print('episode: ', i,'score: ', score)
        done = False
        score = 0
        simulation = SimpleSimulation()
        simulation.disable_normalization()
        observation = simulation.get_current_observation()
        while not done:
            action = agent.choose_action(observation)
            print("Action chose: {}".format(action))
            observation_, reward, done, info = simulation.add_unit(action)
            agent.store_transition(observation, action, reward)
            observation = observation_
            score += reward

        observations.append(simulation.commands)
    for o in observations:
        print(o)
