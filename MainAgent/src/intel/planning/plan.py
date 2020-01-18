from ...utils.units import getUnits
from ...utils.function_utils import agent_method

class Plan:

    
    def __init__(self, goal):
        """
        Assumes goal to be a unit
        """
        self.units = getUnits()
        self.plan  = []
        self.ready_to_proceed = True

        print("Initialize plan for: {}".format(goal))
        self.initializePlan(goal)

    def __len__(self):
        return len(self.plan)

    def initializePlan(self, goal):
        print("Initializing plan for: {}".format(goal))
        current_sub_goal = goal
        while True:
            required = self.units.protossUnits[current_sub_goal]["required"]
            print("Required: {}".format(required))
            can_build = self.units.protossUnits[required]["canBuildFunction"]()
            self.plan.append(required)
            current_sub_goal = required
            if can_build:
                break

    def unlock(self):
        self.ready_to_proceed = True

    @agent_method
    async def execute_next_step(self, agent=None):
        if not self.ready_to_proceed:
            return
        next_goal = self.plan[-1]
        if agent.units(next_goal).ready.exists:
            self.plan.pop()
            return

        print("Next goal: {}".format(next_goal))
        build  = self.units.protossUnits[next_goal]["buildFunction"]
        success = await build(next_goal, self.unlock, True)
 
        if success == True:
            self.ready_to_proceed = False
            self.plan.pop()    

        else:
            print("-------------- EXECUTE NEXT PLAN STEP FAILED ---------------")




    def isFulfilled(self):
        return self.__len__() == 0
