import random
import math
import army_generator

class Evaluator:
    """
    Evaluator creates armies following the array:

    [[type, amount], ...] = 

    [MARINE, MARAUDER, REAPER, HELLION, SIEGETANK, CYCLONE, HELLIONTANK ,
     , ... ]

    """

    def __init__(self, random_army=True, bio_army=True, mech_army=True):
        self.generator_functions = []
        if random_army:
            self.generator_functions.append(small_random_army)
            self.generator_functions.append(medium_random_army)
            self.generator_functions.append(big_random_army)
        if bio_army:
            self.generator_functions.append(bio_army)   
        if mech_army:
            self.generator_functions.append(mech_army)       

        self.max_index = len(self.generator_functions) - 1

        self.army        = None
        self.composition = None
        self.evaluation  = None

        

     
    def generate_enemy_army(self):
        index = random.randint(0, self.max_index+1)
        self.army = self.generator_functions[index]()


    def submit_composition(self, composition):
        """
        composition = [[type, amount], ...]
        """
        self.composition = composition

    def evaluate(self):
        pass           