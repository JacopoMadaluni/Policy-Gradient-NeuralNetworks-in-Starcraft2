from sc2 import run_game, maps, Race, Difficulty, position, Result
from sc2.player import Bot, Computer
from SimulatorAgent import ContinuousSimulatorAgent


if __name__ == "__main__":
    run_game(maps.get("TrainingEnvironment_Continuous"),
            [Bot(Race.Protoss, ContinuousSimulatorAgent()), Computer(Race.Terran, Difficulty.Easy)],
            realtime=False) 