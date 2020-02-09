

from mathematical_model.model import ArmyCompModel
from evaluator import army_generator
from neural_training.Simulations import *

# TOSS UNITS
from sc2.constants import PROBE, ZEALOT, SENTRY, STALKER, ADEPT, HIGHTEMPLAR, DARKTEMPLAR, ARCHON, OBSERVER, WARPPRISM, IMMORTAL, \
                        COLOSSUS, DISRUPTOR, PHOENIX, VOIDRAY, ORACLE, TEMPEST, CARRIER, MOTHERSHIP


if __name__ == "__main__":
    sim = SimpleSimulation()
    model = sim.model
    print(model.utility_of(PHOENIX))
