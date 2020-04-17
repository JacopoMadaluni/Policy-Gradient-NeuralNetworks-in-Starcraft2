from ...utils.units import getUnits
from ...utils.function_utils import agent_method

class Goal:

    """ 
    Goal class represents something that must be achieved (usually a unit).
    """
    def __init__(self, goal):
        """
        Assumes goal to be a unit
        """
        self.units_info = getUnits()
        self.plan  = []
        self.ready_to_proceed = True
        self.initialize_goal(goal)

    def __len__(self):
        return len(self.plan)

    def initialize_goal(self, goal):
        """
        Initializes the sequence of required actions to unlock the input goal.
        These actions are recursively gathered by looking at what the goal requires.
        """
        print("Initializing goal for: {}".format(goal))
        current_sub_goal = goal
        while True:
            required = self.units_info.protossUnits[current_sub_goal]["required"]
            can_build = self.units_info.protossUnits[required]["canBuildFunction"]()
            self.plan.append(required)
            current_sub_goal = required
            if can_build:
                break

    def unlock(self):
        """
        Unlocks the goal to be able to execute the next action.
        """
        self.ready_to_proceed = True

    @agent_method
    async def execute_next_step(self, agent=None):
        """
        Executes the next action in the stack.
        """
        if not self.ready_to_proceed:
            return
        next_goal = self.plan[-1]

        if agent.units_info(next_goal).ready.exists:
            self.plan.pop()
            return

        print("Next sub goal: {}".format(next_goal))
        build  = self.units_info.protossUnits[next_goal]["buildFunction"]
        success = await build(next_goal, self.unlock)
        
 
        if success == True:
            self.ready_to_proceed = False
            self.plan.pop()    

        else:
            print("Execution of goal action failed.")

    def is_fulfilled(self):
        return self.__len__() == 0
