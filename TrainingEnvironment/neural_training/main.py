import tensorflow as tf
from tensorflow import keras
import sc2
import random
import time
import numpy as np
import math
import matplotlib.pyplot as plt 
from sc2 import run_game, maps, Race, Difficulty, position, Result
from sc2.player import Bot, Computer
from PolicyGradient import PolicyGradientAgent




# 165 iterations per minute

class SimulatorAgent(sc2.BotAI):


    def __init__(self, observation):
        self.ITERATIONS_PER_MINUTE = 165
        self.HEADLESS = False

        self.n_zealots   = observation[0]
        self.n_stalkers  = observation[1]
        self.n_immortals = observation[2]

        self.n_marines = observation[3]
        self.n_marauders = observation[4]
        self.n_tanks = observation[5]
        self.n_banshees = observation[6]

    async def on_start_async(self):
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
        pass

    def on_end(self, result):
        print("Game ended")
        print("Result: {}".format(result))
        if result == Result.Victory:
            return 1
        else:
            return 0    

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
            realtime=False)   
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

if __name__ == "__main__":
    agent = PolicyGradientAgent(ALPHA=0.0005, input_dims=7, GAMMA=0.99,
                                n_actions=3, layer1_size=64, layer2_size=64,
                                chkpt_dir='tmp/')
    #agent.load_checkpoint()
    score_history = []
    score = 0
    num_episodes = 3
    #env = wrappers.Monitor(env, "tmp/lunar-lander",
    #                        video_callable=lambda episode_id: True, force=True)
    for i in range(num_episodes):
        print('episode: ', i,'score: ', score)
        done = False
        score = 0
        simulation = Simulation()
        observation = simulation.get_current_observation()
        while not done:
            action = agent.choose_action(observation)
            print(action)
            observation_, reward, done, info = simulation.add_unit(action)
            agent.store_transition(observation, action, reward)
            observation = observation_
            score += reward

        score = simulation.simulate_exchange()    

        print("Result: {}".format(score))
        score_history.append(score)
        agent.learn()
        
        
        agent.save_checkpoint()
    filename = 'testing.png'
    plotLearning(score_history, filename=filename, window=25)






    

