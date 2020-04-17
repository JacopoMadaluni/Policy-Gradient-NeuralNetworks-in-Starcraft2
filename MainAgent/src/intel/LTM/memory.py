from .goal import Goal
from ...utils.function_utils import agent_method

class Memory:

    def __init__(self):
        self.current_goals = {}

    
    def already_tried_to_achieve(self, goal):
        return goal in self.current_goals

    @agent_method
    def record_attempt(self, goal, agent=None):
        self.current_goals[goal] = Goal(goal)

    async def advance(self, goal):
        goal_instance = self.current_goals[goal]
        if not goal_instance.is_fulfilled():
            await goal_instance.execute_next_step()
 

