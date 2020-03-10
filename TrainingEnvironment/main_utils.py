import random
import time
import numpy as np
import math
import matplotlib.pyplot as plt
import threading
import os
from info import *

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
        end = content.find("\n", alpha_i)

        print("{}, {}".format(alpha_i, end))

        alpha = float(content[alpha_i+7: end])

        gamma_i = content.find("GAMMA")
        end = content.find("\n", gamma_i)

        print("{}, {}".format(gamma_i, end))
        gamma = float(content[gamma_i+7: end])

        actions_i = content.find("n_actions")
        end = content.find("\n", actions_i)
        actions = int(content[actions_i + 11: end]) # TODO to fix

        l1_i = content.find("L1")
        end = content.find("\n", l1_i)
        l1 = int(content[l1_i+4: end])

        l2_i = content.find("L2")
        end = content.find("\n", l2_i)
        l2 = int(content[l2_i+4: end])

        input_dims_i = content.find("input_dims")
        end = content.find("\n", input_dims_i)
        input_dims = int(content[input_dims_i+12: end])

        namespace_i = content.find("-$$")
        namespace_end = content.find("$$-")
        ns_string = content[namespace_i+3 : namespace_end]
        namespace = deserialize_namespace(ns_string)

    return alpha, gamma, actions, l1, l2, input_dims, namespace


def get_initial_namespace():
    namespace = []
    print("Press [y/n] to choose which units the agent can use to counter the enemy army.\n\n")
    dictt = name_to_id()
    ok = "n"
    while ok != "y":
        namespace = []
        for name in dictt:
            if input("Use {}? [y/n]\n>".format(name)) == "y":
                namespace.append(dictt[name])
        print("Initialized following namespace: {}".format(namespace))
        ok = input("Proceed? [y/n]")

    serialized = serialize_namespace(namespace)
    return namespace, serialized



def save_info(score_history, agent, win_loss, save_dir):
    win_ratio = (win_loss[0]/(win_loss[0]+win_loss[1]))
    with open(os.path.join(save_dir, "info"), "w+") as f:
        f.write("{}\nWin ratio: {}".format(repr(agent), win_ratio))

    graphname = os.path.join(save_dir, 'graph.png')
    plotLearning(score_history, filename=graphname, window=25)