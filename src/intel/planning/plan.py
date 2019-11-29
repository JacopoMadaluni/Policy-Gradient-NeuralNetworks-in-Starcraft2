from ...utils.units import getUnits
from ...utils.function_utils import agent_method

class Plan:

    
    def __init__(self, goal):
        """
        Assumes goal to be a unit
        """
        self.units = getUnits()
        self.plan  = []
        self.readyToProceed = True

        print("Initialize plan for: {}".format(goal))
        self.initializePlan(goal)

    def __len__(self):
        return len(self.plan)

    def initializePlan(self, goal):
        print("Initializing plan for: {}".format(goal))
        currentSubGoal = goal
        while True:
            required = self.units.protossUnits[currentSubGoal]["required"]
            print("Required: {}".format(required))
            canBuild = self.units.protossUnits[required]["canBuildFunction"]()
            self.plan.append(required)
            currentSubGoal = required
            if canBuild:
                break

    def unlock(self):
        self.readyToProceed = True

    @agent_method
    async def execute_next_step(self, agent=None):
        if not self.readyToProceed:
            return
        nextGoal = self.plan[-1]
        if agent.units(nextGoal).ready.exists:
            self.plan.pop()
            return

        print("Next goal: {}".format(nextGoal))
        build  = self.units.protossUnits[nextGoal]["buildFunction"]
        success = await build(nextGoal, self.unlock, True)
 
        if success == True:
            self.readyToProceed = False
            self.plan.pop()    

        else:
            print("-------------- EXECUTE NEXT PLAN STEP FAILED ---------------")




    def isFulfilled(self):
        return self.__len__() == 0
