from .goal import Goal
from ...utils.function_utils import agent_method

class Memory:

    """
    Main memory class.
    Functions as repository of previously seeked goals.

    The current_goals dictionary contains all the things the 
    agent tried to do in the past but was not able to.
    """
    def __init__(self):
        self.current_goals = {} 

    
    def already_tried_to_achieve(self, goal):
        """
        Returns true if there was a past attempt for the input goal.
        """
        return goal in self.current_goals

    @agent_method
    def record_attempt(self, goal, agent=None):
        """
        Registers a new attempt for the input goal.
        """
        self.current_goals[goal] = Goal(goal)

    async def advance(self, goal):
        """
        Executes the next action in order to achieve the input goal in the future.
        """
        goal_instance = self.current_goals[goal]
        if not goal_instance.is_fulfilled():
            await goal_instance.execute_next_step()
 

