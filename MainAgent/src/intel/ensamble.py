from TrainingEnvironment.info import deserialize_namespace
from TrainingEnvironment.main_utils import load_policy_gradient

from ..utils.function_utils import agent_method

import numpy as np


class GradientEnsamble:

    def __init__(self, gradient_names):
        """
        Ensamble class.
        The gradients in input will be loaded.

        P.S
        It is currently only possible to load one gradient at the time.
        """

        self.gradients = []
        for name in gradient_names:
            # load gradient
            try:
                self.gradients.append(load_policy_gradient(name, "TrainingEnvironment/"))
            except FileNotFoundError as e:
                raise FileNotFoundError("Gradient folder {} does not exist. Aborting.".format(name))    

        print("Initialized gradients: {}".format(gradient_names))    


    @agent_method
    def get_preferred_unit(self, enemy_observation, agent=None):
        """
        Given an observation, it outputs the best unit from the neural network.
        """
        for gradient in self.gradients:
            action_space = deserialize_namespace(gradient.action_namespace)
            amounts = []
            for unit_id in action_space:
                amount = len(agent.units(unit_id))
                amounts.append(amount)

            total = sum(amounts)
            if total == 0:
                total = 1
                
            observation = [a/total for a in amounts]
            observation += enemy_observation
            observation = np.array(observation) # Convert to tensor

            action = gradient.choose_action(observation)
            choosen_unit = action_space[action]
            
            # This return statement should be outside
            # Currently only one gradient is loaded so it's fine.
            return choosen_unit




