from .plan import Plan

class Planner:

    def __init__(self, agent):
        self.agent = agent
        self.current_plans = {}


    def exists_plan_for(self, goal):
        return goal in self.current_plans

    def generate_new_plan(self, goal):
        self.current_plans[goal] = Plan(self.agent, goal)

    async def advance(self, goal):
        try:
            await self.current_plans[goal].execute_next_step()
        except:
            raise Exception("Cannot advance non existing plan for goal: {}".format(goal))    

