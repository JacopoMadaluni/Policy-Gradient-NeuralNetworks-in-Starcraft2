from .plan import Plan
from ...utils.function_utils import agent_method

class Planner:

    def __init__(self):
        self.current_plans = {}

    
    def exists_plan_for(self, goal):
        return goal in self.current_plans

    @agent_method
    def generate_new_plan(self, goal, agent=None):
        self.current_plans[goal] = Plan(goal)

    async def advance(self, goal):
        try:
            await self.current_plans[goal].execute_next_step()
        except KeyError:
            raise Exception("Cannot advance non existing plan for goal: {}".format(goal))    

