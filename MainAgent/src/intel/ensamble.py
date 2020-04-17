from TrainingEnvironment.info import deserialize_namespace
from TrainingEnvironment.main_utils import load_policy_gradient

from ..utils.function_utils import agent_method

import numpy as np


class GradientEnsamble:

    def __init__(self, gradient_names):

        self.gradients = []
        for name in gradient_names:
            # load gradient
            self.gradients.append(load_policy_gradient(name, "TrainingEnvironment/"))

        print("Initialized gradients: {}".format(gradient_names))    


    @agent_method
    def get_preferred_unit(self, enemy_observation, agent=None):
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
            observation = np.array(observation)

            action = gradient.choose_action(observation)
            choosen_unit = action_space[action]
            return choosen_unit




