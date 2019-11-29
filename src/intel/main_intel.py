import random
import numpy as np

from ..utils.units import getUnits
from ..utils.constants import *
from ..utils.function_utils import agent_method
          
from ..utils.constants             import *
from ..utils.units                 import Units      
from ..utils.logic                 import getLogic

from .planning.plan         import Plan
from .planning.planner      import Planner
from .visualizer            import Visualizer
from .attack_engine         import Attacker
from .scouting              import Scouter

from ..learning.cnn.training_data  import Trainer 

class Intel:

    def __init__(self, agent):
        self.agent = agent
        
        

        self.current_mode = 0
        self.performed_actions = set()
        self.modes = {
            0: self.economy_mode,
            1: self.make_army_mode,
            2: self.attack_mode
        }

        self.plan = None
        self.planner    = Planner()
        self.trainer    = Trainer()
        self.visualizer = Visualizer()
        self.attacker   = Attacker(self.visualizer, self.trainer)
        self.scouter    = Scouter()

    async def act(self, iteration):
        agent = self.agent
        #await self.testing()
        self.visualizer.draw_information()
        agent.iteration = iteration
        agent.current_minute = iteration / agent.ITERATIONS_PER_MINUTE      
        await self.modes[self.current_mode]()
        await self.scout()
        self.current_mode = (self.current_mode + 1) % 3

    async def economy_mode(self):
        await self.build_workers()
        await self.distribute_workers()
        await self.build_pylons()
        await self.build_assimilators()
        await self.expand()   
        
    async def make_army_mode(self):
        await self.advance_tech()
        await self.research_upgrades()
        await self.build_army()
        await self.warp_army()    

    async def attack_mode(self):
        await self.attacker.attack_with_model()
        #await self.attack()    

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
                    await agent.build(PYLON, near=nexuses.first, max_distance=500)
    
    @agent_method
    async def build_assimilators(self, agent=None):
        if agent.supply_used < 14:
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
        if len(agent.units(OBSERVER)) > 0:
            observer = agent.units(OBSERVER)[0]
            await self.scouter.scout_enemy_base(observer)
        else:
            """ Build observer """
            if agent.units(ROBOTICSFACILITY).ready.exists:
                for rf in agent.units(ROBOTICSFACILITY).ready.noqueue:
                    if agent.can_afford(OBSERVER) and agent.supply_left > 0:
                        await agent.do(rf.train(OBSERVER))
                        break
            elif self.planner.exists_plan_for(OBSERVER):
                await self.planner.advance(OBSERVER)
            else:
                self.planner.generate_new_plan(OBSERVER)    

        
        #await self.scouter.scout_map()


        
    @agent_method
    async def expand(self, agent=None):
        if agent.units(NEXUS).amount < 3 and agent.can_afford(NEXUS):
            await agent.expand_now()

    @agent_method
    async def advance_tech(self, agent=None):
        if agent.units(PYLON).ready.exists:
            pylon = agent.units(PYLON).ready.random
            """if self.units(GATEWAY).ready.exists and not self.units(CYBERNETICSCORE).exists:
                if self.can_afford(CYBERNETICSCORE) and not self.already_pending(CYBERNETICSCORE):
                    await self.build(CYBERNETICSCORE, near=pylon)"""
            if len(agent.units(GATEWAY)) < agent.current_minute:
                if agent.can_afford(GATEWAY) and not agent.already_pending(GATEWAY):
                    await agent.build(GATEWAY, near=pylon)

            """if self.units(CYBERNETICSCORE).ready.exists:
                if self.current_minute > 3 and self.units(STARGATE).amount < 2:
                    if self.can_afford(STARGATE) and not self.already_pending(STARGATE):
                        await self.build(STARGATE, near=pylon)"""

    @agent_method
    async def research_upgrades(self, agent=None):
        
        if agent.units(CYBERNETICSCORE).ready.exists and agent.can_afford(RESEARCH_WARPGATE) and RESEARCH_WARPGATE not in self.performed_actions:
            #print(dir(self.units(CYBERNETICSCORE)[0]))
            cybercore = agent.units(CYBERNETICSCORE).ready.first
            await agent.do(cybercore(RESEARCH_WARPGATE))        
            self.performed_actions.add(RESEARCH_WARPGATE)        

    
    @agent_method
    async def build_army(self, agent=None):
        for gateway in agent.units(GATEWAY).ready.noqueue:
            if not agent.units(STALKER).amount > agent.units(VOIDRAY).amount:
                if agent.units(CYBERNETICSCORE).ready.exists and agent.can_afford(STALKER) and agent.supply_left > 2:
                    if random.uniform(0, 1) > 0.8:
                        await agent.do(gateway.train(SENTRY))
                    else:
                        await agent.do(gateway.train(STALKER))
                
        for stargate in agent.units(STARGATE).ready.noqueue:
            if agent.can_afford(VOIDRAY) and agent.supply_left > 3:
                await agent.do(stargate.train(VOIDRAY))

        for rf in agent.units(ROBOTICSFACILITY).ready.noqueue:
            if agent.can_afford(IMMORTAL) and agent.supply_left > 4:
                await agent.do(rf.train(IMMORTAL))        

    @agent_method
    async def warp_army(self, agent=None):
        if agent.units(PYLON):
            pylon = random.choice(agent.units(PYLON))
        for warpgate in agent.units(WARPGATE).ready:
            can_warp = await agent.get_available_abilities(warpgate)
            if AbilityId.WARPGATETRAIN_STALKER in can_warp:
                warp_location = pylon.position.to2.random_on_distance(4)
                placement = await agent.find_placement(AbilityId.WARPGATETRAIN_STALKER, warp_location, placement_step=1)
                if placement is None:
                    print("could not warp")
                    return
                await agent.do(warpgate.warp_in(STALKER, placement))    


    @agent_method
    def find_target(self, unit, agent=None):
        if len(agent.known_enemy_units) > 0:
            return agent.known_enemy_units.closest_to(unit)
        elif len(agent.known_enemy_structures) > 0:
            return random.choice(agent.known_enemy_structures)
        else:
            return agent.enemy_start_locations[0]

    @agent_method
    async def full_attack(self, army, agent=None):
        for UNIT_TYPE in army:
            UNITS = agent.units(UNIT_TYPE)
            for UNIT in UNITS.idle:
                await agent.do(UNIT.attack(agent.find_target(UNIT)))

    @agent_method
    async def attack(self, agent=None):
        # {UNIT : [n to attack, n to defend]}
        army = {STALKER : [15, 1],
                VOIDRAY : [8, 1]}

        for UNIT in army:
            if agent.units(UNIT).amount > army[UNIT][1]:
                #defend
                if len(agent.known_enemy_units) > 0:
                    target = agent.known_enemy_units.closest_to(agent.units(UNIT)[0])
                    #print(dir(target))
                    if target.is_attacking:
                        print("target is attacking")
                        for s in agent.units(UNIT).idle:
                            await agent.do(s.attack(target))

            elif agent.units(UNIT).amount > army[UNIT][0]:
                #for s in self.units(UNIT).idle:
                #    await self.do(s.attack(self.find_target(self.state)))
                await self.full_attack(army)
#        if self.units(STALKER).amount > 15:
#            for s in self.units(STALKER).idle:
#                await self.do(s.attack(self.find_target(self.state)))
#        elif self.units(STALKER).amount > 3:
#            if len(self.known_enemy_units) > 0:
#                for s in self.units(STALKER).idle:
#                    await self.do(s.attack(random.choice(self.known_enemy_units)))

    