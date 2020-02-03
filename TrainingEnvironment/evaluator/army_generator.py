import sys
sys.path.append('C:\\Users\Jaco\Documents\\__FinalProject\\MainAgent\\TrainingEnvironment')
from info import *
import random
import math

terran_units = terran_units()

def random_army(number_of_different_units, min_supply, max_supply):
    total_supply = random.randint(min_supply, max_supply)
    print(total_supply)
    units_to_pick = number_of_different_units
    units = []
    while units_to_pick != 0:
        for unit in terran_units:
            if terran_units[unit]["disabled"]:
                continue
            if random.uniform(0, 1) > 0.9:
                units.append(unit)
                units_to_pick -= 1
            if units_to_pick == 0:
                break

    composition = []
    for i, unit_type in enumerate(units): 
        unit = terran_units[unit_type]
        if unit["supply"] > total_supply:
            break
        amount = 0
        if i == len(units)-1:
            # last unit, allocate all remaining supply
            amount = math.floor(total_supply / unit["supply"])
        else:
            allocated_supply = random.randint(unit["supply"], total_supply)   
            amount = math.floor(allocated_supply / unit["supply"])
     
        composition.append([unit_type, amount])
        total_supply -= allocated_supply

    return composition        

def small_random_army():
    return random_army(3, 10, 20)

def medium_random_army():
    return random_army(4, 20, 40)

def big_random_army():
    return random_army(6, 60, 70)

def bio_army(size):
    supply = size
    n_medivacs = 0
    if size > 20:
        n_medivacs = 2
    if size > 40:    
        n_medivacs = 3
    if size > 60:
       n_medivacs = 4

    medivac_supply = n_medivacs * 2
    supply -= medivac_supply
    n_marines   = random.randint(10, supply/2)
    n_marauders = math.floor((supply - n_marines)/2)

    return [[MARINE, n_marines], [MARAUDER, n_marauders], [MEDIVAC, n_medivacs]]

def mech_army(size):
    pass                


if __name__ == "__main__":
    print(bio_army(40))
