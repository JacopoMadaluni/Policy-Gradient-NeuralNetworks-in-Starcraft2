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
from sc2 import run_game, maps, Race, Difficulty, position, Result
from sc2.player import Bot, Computer
from neural_training.PolicyGradient import PolicyGradientAgent
from neural_training.Simulations import SimpleSimulation, HardSimulation


hard_simulation_initial_namespace = [ZEALOT, STALKER, ADEPT, IMMORTAL, COLOSSUS, VOIDRAY, ARCHON]

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
    else:
        os.mkdir(full_dir_location)

    return simulation_location, load_checkpoint

def get_agent_settings(simulation_dir):
    info_path = os.path.join(simulation_dir, "info")

    alpha = None
    gamma = None
    actions = None
    l1 = None
    l2 = None
    input_dims = None
    namespace = None

    with open(info_path, "r") as info_file:
        content = info_file.read()

        alpha_i = content.find("ALPHA")
        alpha = float(content[alpha_i+7: alpha_i+7+7])

        gamma_i = content.find("GAMMA")
        gamma = float(content[gamma_i+7: gamma_i+7+4])

        actions_i = content.find("n_actions")
        actions = int(content[actions_i+11])

        l1_i = content.find("L1")
        l1 = int(content[l1_i+4: l1_i+4+2])

        l2_i = content.find("L2")
        l2 = int(content[l2_i+4: l2_i+4+2])

        input_dims_i = content.find("input_dims")
        input_dims = int(content[input_dims_i+12: input_dims_i+12+2])

        namespace_i = content.find("-$$")
        namespace_end = content.find("$$-")
        ns_string = content[namespace_i+3 : namespace_end]
        namespace = deserialize_namespace(ns_string)

    return alpha, gamma, actions, l1, l2, input_dims, namespace


def get_initial_namespace():
    namespace = []
    print("Press [y/n] to choose which units the agent can use to counter the enemy army.\n\n")
    dictt = name_to_id()
    for name in dictt:
        if input("Use {}? [y/n]\n>".format(name)) == "y":
            namespace.append(dictt[name])
    print("Initialized following namespace: ")
    print(namespace)
    serialized = serialize_namespace(namespace)
    return namespace, serialized



def save_info(agent, win_loss, save_dir):
    win_ratio = (win_loss[0]/(win_loss[0]+win_loss[1]))
    with open(os.path.join(save_dir, "info"), "w+") as f:
        f.write("{}\nWin ratio: {}".format(repr(agent), win_ratio))

    graphname = os.path.join(save_dir, 'graph.png')
    plotLearning(score_history, filename=graphname, window=25)

if __name__ == "__main__":
    checkpoints_dir = "neural_training/checkpoints/"
    simulation_location, load_checkpoint = get_user_inputs(checkpoints_dir)
    simulation_dir = os.path.join(checkpoints_dir, simulation_location)


    agent = None
    namespace = None # default

    if load_checkpoint:
        alpha, gamma, actions, l1, l2, input_dims, namespace = get_agent_settings(simulation_dir)
        namespace_serialized = serialize_namespace(namespace)
        agent = PolicyGradientAgent(ALPHA=alpha, input_dims=input_dims, GAMMA=gamma,
                                n_actions=actions, layer1_size=l1, layer2_size=l2,
                                chkpt_dir=simulation_dir, action_namespace=namespace_serialized)
        agent.load_checkpoint()
        print("Checkpoint successfully loaded with following settings:")
        print(agent)

    else:
        namespace, namespace_serialized = get_initial_namespace()
        n_actions = len(namespace)
        input_dims = n_actions + n_active_terran_units()
        agent = PolicyGradientAgent(ALPHA=0.0001, input_dims=input_dims, GAMMA=0.99,
                                n_actions=n_actions, layer1_size=64, layer2_size=64,
                                chkpt_dir=simulation_dir, action_namespace=namespace_serialized)

    score_history = []
    win_loss = [0, 0]
    score = 0
    num_episodes = int(input("How many simulations?\n> "))

    for i in range(num_episodes):
        print('episode: ', i,'score: ', score)
        done = False
        score = 0
        #simulation = SimpleSimulation()
        simulation = HardSimulation(namespace)
        observation = simulation.get_current_observation()
        while not done:
            action = agent.choose_action(observation)
            print("Action chose: {}".format(action))
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
        del simulation

    save_info(agent, win_loss, simulation_dir)
