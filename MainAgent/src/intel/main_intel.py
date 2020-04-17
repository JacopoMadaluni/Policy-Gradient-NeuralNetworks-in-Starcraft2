import random
import numpy as np

from ..utils.units import getUnits
from ..utils.constants import *
from ..utils.function_utils import agent_method
          
from ..utils.constants             import *
from ..utils.units                 import getUnits      
from ..utils.logic                 import getLogic
from ..utils.map_area              import MapArea
from ..utils.map_area              import compute_no_construction_areas

from .LTM.memory            import Memory 
from .visualizer            import Visualizer
from .scouting              import Scouter
from .belief                import Belief
from .ensamble              import GradientEnsamble


class Intel:

    def __init__(self, agent):
        self.agent = agent
        self.units_info = getUnits()
        

        self.current_mode = 0
        self.performed_actions = set()
        self.modes = {
            0: self.economy_mode,
            1: self.make_army_mode,
            2: self.attack_mode
        }

        self.bad_locations = []

        self.memory     = Memory()
        self.visualizer = Visualizer()
        self.scouter    = Scouter()
        self.belief     = Belief() 
        self.ensamble   = GradientEnsamble(["128_128_hard_no_air_6_highrewards"])

        self.attacking = False
        self.grouped   = False


    @agent_method
    async def act(self, iteration, agent=None):

        self.visualizer.set_bad_areas(self.bad_locations)
        self.visualizer.draw_information()
        agent.iteration = iteration
        agent.current_minute = iteration / agent.ITERATIONS_PER_MINUTE      

        await self.standard_mode()
        await self.modes[self.current_mode]()
        self.current_mode = (self.current_mode + 1) % 3

    async def standard_mode(self):
        self.update_no_contruction_areas()
        await self.scout()
        await self.update_belief()

    async def economy_mode(self):
        await self.build_workers()
        await self.distribute_workers()
        await self.build_pylons()
        await self.build_assimilators()
        await self.expand()   
        
    async def make_army_mode(self):
        await self.build_gateways()
        await self.research_upgrades()
        await self.warp_army()    

    async def attack_mode(self):
        await self.regroup_army()
        await self.attack()  
    

    @agent_method
    def update_no_contruction_areas(self, agent=None):
        if len(agent.units(NEXUS)) > len(self.bad_locations):
            self.bad_locations = compute_no_construction_areas()    


    @agent_method
    async def update_belief(self, agent=None):
        if len(agent.known_enemy_units) > 0:
            self.belief.update()

    @agent_method
    async def distribute_workers(self, agent=None):
        try:
            await agent.distribute_workers()
        except ValueError:
            print("Value error in distribute_workers()")

    @agent_method
    async def build_workers(self, agent=None):
        if agent.units(PROBE).amount < agent.MAX_WORKERS:
            for nexus in agent.units(NEXUS).ready.noqueue:
                if agent.can_afford(PROBE) and agent.state.units(PROBE).closer_than(5.0, nexus).amount < 16:
                    await agent.do(nexus.train(PROBE))

    @agent_method
    async def build_pylons(self, agent=None):
        if ((not agent.units(PYLON).ready.exists and not agent.already_pending(PYLON)) or
            (agent.supply_left < 5 and not agent.already_pending(PYLON))):
            nexuses = agent.units(NEXUS).ready
            if nexuses.exists:
                if agent.can_afford(PYLON):
                    location = None
                    while True:
                        location = random.choice(agent.units(NEXUS)).position.to2.random_on_distance(4)
                        if not self.bad_locations[0].contains(location):
                            break
                    placement = await agent.find_placement(PYLON, location, placement_step=1)
                    await agent.build(PYLON, near=placement, max_distance=1)
    
    @agent_method
    async def build_assimilators(self, agent=None):
        if agent.supply_workers < 14:
            return
        for nexus in agent.units(NEXUS).ready:
            vespenes = agent.state.vespene_geyser.closer_than(15.0, nexus)
            for vespene in vespenes:
                if not agent.can_afford(ASSIMILATOR):
                    break
                if not agent.units(ASSIMILATOR).closer_than(1.0, vespene).exists:
                    worker = agent.select_build_worker(vespene.position)
                    if not worker:
                        break
                    await agent.do(worker.build(ASSIMILATOR, vespene))

    @agent_method                
    async def scout(self, agent=None):
        # Try to scout the enemy base for information
        if len(agent.units(OBSERVER)) > 0:
            observer = agent.units(OBSERVER)[0]
            await self.scouter.scout_enemy_base(observer)
        else:
            # An observer is needed
            observer_info = self.units_info.protossUnits[OBSERVER]
            can_build_function = observer_info["canBuildFunction"]
            if can_build_function():
                build = observer_info["buildFunction"]
                await build()
            elif self.memory.already_tried_to_achieve(OBSERVER):
                await self.memory.advance(OBSERVER)
            else:
                self.memory.record_attempt(OBSERVER)    

        # Scout the map
        await self.scouter.scout_map()


        
    @agent_method
    async def expand(self, agent=None):
        if agent.units(NEXUS).amount < 3 and agent.can_afford(NEXUS):
            await agent.expand_now()

    @agent_method
    async def build_gateways(self, agent=None):
        if len(agent.units(GATEWAY)) > 9:
            return
        if agent.units(PYLON).ready.exists:
            pylon = agent.units(PYLON).ready.random
            if len(agent.units(GATEWAY)) < agent.current_minute:
                if agent.can_afford(GATEWAY) and not agent.already_pending(GATEWAY):
                    location = None
                    while True:
                        location = pylon.position.to2.random_on_distance(4)
                        if not self.bad_locations[0].contains(location):
                            break
                    placement = await agent.find_placement(GATEWAY, location, placement_step=1)
                    await agent.build(GATEWAY, near=placement, max_distance = 1)

    @agent_method
    async def research_upgrades(self, agent=None):       
        if agent.units(CYBERNETICSCORE).ready.exists and agent.can_afford(RESEARCH_WARPGATE) and RESEARCH_WARPGATE not in self.performed_actions:
            cybercore = agent.units(CYBERNETICSCORE).ready.first
            await agent.do(cybercore(RESEARCH_WARPGATE))        
            self.performed_actions.add(RESEARCH_WARPGATE)     
        if agent.units(TWILIGHTCOUNCIL).ready.exists and agent.can_afford(RESEARCH_CHARGE)and RESEARCH_CHARGE not in self.performed_actions:
            council = agent.units(TWILIGHTCOUNCIL).ready.first   
            await agent.do(council(RESEARCH_CHARGE))
            self.performed_actions.add(RESEARCH_CHARGE)   

    @agent_method
    async def warp_army(self, agent=None):
        preferred_unit = self.ensamble.get_preferred_unit(self.belief.get_normalized_belief_as_array())   
        print("Preferred unit: {}".format(preferred_unit))     
        unit_info = self.units_info.get_protoss_units()[preferred_unit]
        
        can_build = unit_info["canBuildFunction"]
        if can_build():
            build_unit = unit_info["buildFunction"]
            await build_unit()
        else:
            if self.memory.already_tried_to_achieve(preferred_unit):
                await self.memory.advance(preferred_unit)
            else:
                self.memory.record_attempt(preferred_unit)
                await self.memory.advance(preferred_unit)


    @agent_method
    async def regroup_army(self, agent=None):
        if not self.grouped:
            rally_location = self.scouter.variances.position_variance(agent.game_info.map_size, 
                                                    random.choice(agent.units(NEXUS)).position)
            for u_type in self.units_info.get_protoss_units():
                for unit in agent.units(u_type).idle:
                    await agent.do(unit.move(rally_location))
            self.grouped = True        

    @agent_method
    def find_target(self, unit, agent=None):
        if len(agent.known_enemy_units) > 0:
            return agent.known_enemy_units.closest_to(unit)
        elif len(agent.known_enemy_structures) > 0:
            return random.choice(agent.known_enemy_structures)
        else:
            return agent.enemy_start_locations[0]

    @agent_method
    async def full_attack(self, agent=None):
        for u_type in self.units_info.get_protoss_units():
            if u_type == PROBE:
                continue
            units = agent.units(u_type)
            for unit in units:
                await agent.do(unit.attack(self.find_target(unit)))    

    @agent_method
    async def defend(self, agent=None):
        if len(agent.known_enemy_units) > 0:
            random_nexus = random.choice(agent.units(NEXUS))
            target = agent.known_enemy_units.closest_to(random_nexus)
            closest_nexus = agent.units(NEXUS).closest_to(target)
            if target.distance_to(closest_nexus) < 20:
                for u_type in self.units_info.get_protoss_units():
                    if u_type == PROBE:
                        continue
                    for unit in agent.units(u_type).idle:
                        await agent.do(unit.attack(target))
                self.grouped = False        

    @agent_method
    async def attack(self, agent=None):
        if agent.supply_army < 10:
            self.attacking = False

        await self.defend()
        
        if agent.supply_army > 50 or self.attacking:
            self.attacking = True
            await self.full_attack()


    