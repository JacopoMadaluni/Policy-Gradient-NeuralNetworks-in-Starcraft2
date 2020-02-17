

from mathematical_model.model import ArmyCompModel
from evaluator import army_generator
from neural_training.Simulations import *

# TOSS UNITS
from sc2.constants import PROBE, ZEALOT, SENTRY, STALKER, ADEPT, HIGHTEMPLAR, DARKTEMPLAR, ARCHON, OBSERVER, WARPPRISM, IMMORTAL, \
                        COLOSSUS, DISRUPTOR, PHOENIX, VOIDRAY, ORACLE, TEMPEST, CARRIER, MOTHERSHIP


if __name__ == "__main__":
    sim = HardSimulation()
    model = sim.model
    print("------> model choice: {}".format(model.units[0]))
    while sim.ready == False:
        sim.add_unit(4)
    print(sim.get_current_observation())    
    print("Number of features: {}".format(len(sim.get_current_observation())))
    print("Number of actions: {}".format(sim.n_of_ally_different_units))
    #sim.simulate_exchange()

        
    
