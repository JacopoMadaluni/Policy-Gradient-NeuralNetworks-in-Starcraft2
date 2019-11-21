from ...utils.units import getUnits
class Plan:

    
    def __init__(self, agent, goal):
        """
        Assumes goal to be a unit
        """
        self.units = getUnits()
        self.agent = agent
        self.plan  = []
        self.readyToProceed = True

        print("Initialize plan for: {}".format(goal))
        self.initializePlan(goal)

    def __len__(self):
        return len(self.plan)

    def initializePlan(self, goal):
        #self.plan.append(goal)
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

    async def execute_next_step(self):
        if not self.readyToProceed:
            return
        nextGoal = self.plan[-1]
        print("Next goal: {}".format(nextGoal))
        build  = self.units.protossUnits[nextGoal]["buildFunction"]
        success = await build(nextGoal, self.unlock, True)
        #if success == 2:
        #    print("plan in progress...")
        #    self.readyToProceed = False
        if success == True:
            self.readyToProceed = False
            self.plan.pop()    

        else:
            print("-------------- EXECUTE NEXT PLAN STEP FAILED ---------------")




    def isFulfilled(self):
        return self.__len__() == 0
