
import sys
from sc2 import run_game, maps, Race, Difficulty, position, Result
from sc2.player import Bot, Computer
from MainAgent.main import MainAgent

if __name__ == "__main__":
    diffs = {"easy": Difficulty.Easy, "medium": Difficulty.Medium, "hard": Difficulty.Hard, "vhard": Difficulty.VeryHard}
    difficulty = None
    realtime = False
    try:
        inp = input("Input difficulty [easy, medium, hard, vhard]\n> ").lower()
        realtime = False if input("Do you want the game to be speed up? [y,n]\n> ").lower() == "y" else True
        difficulty = diffs[inp]
    except KeyError:
        print("The selected difficulty \"{}\" doesn't exist, please choose between [easy, medium, hard, vhard]".format(inp))
        sys.exit(0)

    run_game(maps.get("AbyssalReefLE"),
            [Bot(Race.Protoss, MainAgent()), Computer(Race.Terran, difficulty)],
            realtime=realtime)