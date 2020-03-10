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
from info import *
from main_utils import *
from sc2 import run_game, maps, Race, Difficulty, position, Result
from sc2.player import Bot, Computer
from neural_training.QLearningAgent import QLearningAgent
from neural_training.Simulations import SimpleSimulation, HardSimulation


hard_simulation_initial_namespace = [ZEALOT, STALKER, ADEPT, IMMORTAL, COLOSSUS, VOIDRAY, ARCHON]


if __name__ == "__main__":
    checkpoints_dir = "neural_training/checkpoints/"
    simulation_location, load_checkpoint = get_user_inputs(checkpoints_dir)
    simulation_dir = os.path.join(checkpoints_dir, simulation_location)


    agent = None
    namespace = None # default

    if load_checkpoint:
        alpha, gamma, actions, l1, l2, input_dims, namespace = get_agent_settings(simulation_dir)
        namespace_serialized = serialize_namespace(namespace)
        agent = QLearningAgent(ALPHA=alpha, input_dims=input_dims, GAMMA=gamma,
                                n_actions=actions, layer1_size=l1, layer2_size=l2,
                                chkpt_dir=simulation_dir, action_namespace=namespace_serialized)
        agent.load_checkpoint()
        print("Checkpoint successfully loaded with following settings:")
        print(agent)

    else:
        namespace, namespace_serialized = get_initial_namespace()
        n_actions = len(namespace)
        input_dims = 1 + n_actions + n_active_terran_units()
        agent = QLearningAgent(ALPHA=0.01, input_dims=input_dims, GAMMA=0.99,
                                n_actions=n_actions, layer1_size=128, layer2_size=128,
                                chkpt_dir=simulation_dir, action_namespace=namespace_serialized)

    score_history = []
    eps_history = []
    win_loss = [0, 0]
    score = 0
    scores = []

    num_episodes = int(input("How many simulations?\n> "))

    for i in range(num_episodes):

        print('episode: ', i,'score: ', score)
        done = False
        score = 0
        

        simulation = HardSimulation(namespace)
        observation = simulation.get_current_observation()
        while not done:
            action = agent.choose_action(observation)
            print("Action chose: {}".format(action))
            observation_, reward, done, info = simulation.add_unit(action)
            agent.store_transition(observation, action, reward, observation_, int(done))
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
        eps_history.append(agent.e)

        agent.learn()

        agent.save_checkpoint()
        del simulation

        if i%100 == 0:
            save_info(score_history, agent, win_loss, simulation_dir)

    save_info(score_history, agent, win_loss, simulation_dir)