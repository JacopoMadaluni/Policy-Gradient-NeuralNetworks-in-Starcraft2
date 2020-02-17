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
        u = random.choice(list(terran_units))
        if u not in units and terran_units[u]["disabled"] == False:
           units.append(u)
           units_to_pick -= 1 


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
    n_marines   = random.randint(10, math.floor(supply/2))
    supply -= medivac_supply
    n_marauders = math.floor((supply - n_marines)/2)

    return [[MARINE, n_marines], [MARAUDER, n_marauders], [MEDIVAC, n_medivacs]]

def mech_army(size):
    assert (size % 5) == 0
    supply = size
    supply_each = size/5

    n_hellbats = math.floor(supply_each/terran_units[HELLIONTANK]["supply"])
    n_cyclones = math.floor(supply_each/terran_units[CYCLONE]["supply"])
    n_tanks    = math.floor(supply_each/terran_units[SIEGETANK]["supply"])
    n_thors    = math.floor(supply_each/terran_units[THOR]["supply"])
    n_vikings  = math.floor(supply_each/terran_units[VIKING]["supply"])

    return [[HELLIONTANK, n_hellbats], [CYCLONE, n_cyclones], [SIEGETANK, n_tanks], [THOR, n_thors], [VIKING, n_vikings]]                


if __name__ == "__main__":
    print(bio_army(40))
