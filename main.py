import sc2
import random
import time
import numpy as np
from sc2 import run_game, maps, Race, Difficulty, position, Result
from sc2.player import Bot, Computer
               

from src.utils.initializer    import *     
from src.utils.function_utils import initialize_function_utils
from src.intel.main_intel     import Intel



# 165 iterations per minute

class AlphaStar(sc2.BotAI):


    def __init__(self):
        self.ITERATIONS_PER_MINUTE = 165
        self.MAX_WORKERS = 80
        self.HEADLESS = False
        """ INITIALIZATION """
        initialize_function_utils(self)
        init_logic_modules(self)
        self.intel      = Intel(self)
        

        

    async def on_step(self, iteration):
        await self.intel.act(iteration)

    def on_end(self, result):
        print("Game ended")
        print("Result: {}".format(result))
        if result == Result.Victory:
            np.save("data/training_data/{}.npy".format(str(int(time.time()))), np.array(self.trainer.attack_training_data))

    


if __name__ == "__main__":
    run_game(maps.get("AbyssalReefLE"),
            [Bot(Race.Protoss, AlphaStar()), Computer(Race.Terran, Difficulty.Easy)],
            realtime=True)
