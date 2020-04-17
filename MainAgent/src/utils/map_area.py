from .constants import *
from .function_utils import agent_method

class MapArea:

    """
    This object represent a square portion of the map.
    """
    def __init__(self, min_x, min_y, max_x, max_y):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.locations = self._compute_locations()

    def __repr__(self):
        return "x: {}-{}, y: {}-{}".format(self.min_x, self.max_x, self.min_y, self.max_y)

    def __iter__(self):
        """
        Iterates through all the points in the area.
        The points are stored in the self.locations list object
        """
        for l in self.locations:
            yield l    

    def _compute_locations(self):
        """
        Computes all the points in the area.
        Executed after __init__
        """
        locations = []
        for x in range(int(self.min_x), int(self.max_x)):
            for y in range(int(self.min_y), int(self.max_y)):
                locations.append([x, y])
        return locations        

    def contains(self, position):
        """
        Returns True if the MapArea contains the input position.
        Position = (x, y)
        """
        x = position[0]
        y = position[1]

        return (x >= self.min_x and x <= self.max_x and \
                y >= self.min_y and y <= self.max_y)


@agent_method
def compute_no_construction_areas(agent=None):
    """
    Utility function.
    Used to compute areas between nexuses and mineral lines.
    
    returns: List[MapArea]
    """
    bad_locations = []
    for nexus in agent.units(NEXUS):
        to_print = ""

        min_x = 0
        min_y = 0
        max_x = 0
        max_y = 0
        flag = False
        
        for field in agent.state.mineral_field.closer_than(15.0, nexus):
            x = field.position[0]
            y = field.position[1]
            if not flag:
                min_x = x
                max_x = x
                min_y = y
                max_y = y
                flag = True
                continue
            if x > max_x:
                max_x = x
            elif x < min_x:
                min_x = x
            if y > max_y:
                max_y = y
            elif y < min_y:
                min_y = y                

        nexus_x = nexus.position[0]
        nexus_y = nexus.position[1] 
        if nexus_x > max_x:
            max_x = nexus_x
        elif nexus_x < min_x:
            min_x = nexus_x
        if nexus_y > max_y:
            max_y = nexus_y
        elif nexus_y < min_y:
            min_y = nexus_y
            
        bad_area = MapArea(min_x-2, min_y-2, max_x+2, max_y+2)

        bad_locations.append(bad_area)  
    
    return bad_locations                
                