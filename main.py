import sc2
import random
from sc2 import run_game, maps, Race, Difficulty, position
from sc2.player import Bot, Computer
               
from src.utils.initializer         import *               
from src.utils.constants           import *
from src.utils.units               import Units                    
from src.intel.planning.plan       import Plan
from src.intel.planning.planner    import Planner
from src.utils.logic               import getLogic
from src.intel.visualizer          import Visualizer


# 165 iterations per minute

class AlphaStar(sc2.BotAI):

    async def testing(self):
        #f = self.units_logic.protossUnits[COLOSSUS]["canBuildFunction"]
        #print(f())
        if self.plan is None:
            self.plan = Plan(self, COLOSSUS)
        await self.build_assimilators()
        await self.build_pylons()
        await self.distribute_workers()
        if not self.plan.isFulfilled():
            await self.plan.executeNextAction()
            
            
            

        if getLogic(self).can_build(COLOSSUS):
            print("Plan goal achieved!")
            await getLogic(self).buildColossus()

    def __init__(self):
        self.ITERATIONS_PER_MINUTE = 165
        self.MAX_WORKERS = 80
        """ INITIALIZATION """
        init_logic_modules(self)

        self.plan = None
        self.planner = Planner(self)

        self.visualizer = Visualizer(self)
         



        self.current_mode = 0
        self.performed_actions = set()
        self.modes = {
            0: self.economy_mode,
            1: self.make_army_mode,
            2: self.attack_mode
        }

    async def on_step(self, iteration):
        #await self.testing()
        self.visualizer.draw_information()
        self.iteration = iteration
        self.current_minute = iteration / self.ITERATIONS_PER_MINUTE      
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
        await self.attack()    

    async def build_workers(self):
        if self.units(PROBE).amount < self.MAX_WORKERS:
            for nexus in self.units(NEXUS).ready.noqueue:
                if self.can_afford(PROBE) and self.state.units(PROBE).closer_than(5.0, nexus).amount < 16:
                    await self.do(nexus.train(PROBE))

    async def build_pylons(self):
        if self.supply_left < 5 and not self.already_pending(PYLON):
            nexuses = self.units(NEXUS).ready
            if nexuses.exists:
                if self.can_afford(PYLON):
                    await self.build(PYLON, near=nexuses.first, max_distance=40)

    async def build_assimilators(self):
        for nexus in self.units(NEXUS).ready:
            vespenes = self.state.vespene_geyser.closer_than(15.0, nexus)
            for vespene in vespenes:
                if not self.can_afford(ASSIMILATOR):
                    break
                if not self.units(ASSIMILATOR).closer_than(1.0, vespene).exists:
                    worker = self.select_build_worker(vespene.position)
                    if not worker:
                        break
                    await self.do(worker.build(ASSIMILATOR, vespene))

    def random_location_variance(self, enemy_start_location):
        x = enemy_start_location[0]
        y = enemy_start_location[1]

        x += ((random.randrange(-20, 20))/100) * enemy_start_location[0]
        y += ((random.randrange(-20, 20))/100) * enemy_start_location[1]

        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > self.game_info.map_size[0]:
            x = self.game_info.map_size[0]
        if y > self.game_info.map_size[1]:
            y = self.game_info.map_size[1]

        go_to = position.Point2(position.Pointlike((x,y)))
        return go_to                

    async def scout(self):
        if len(self.units(OBSERVER)) > 0:
            scout = self.units(OBSERVER)[0]
            if scout.is_idle:
                enemy_location = self.enemy_start_locations[0]
                move_to = self.random_location_variance(enemy_location)
                print(move_to)
                await self.do(scout.move(move_to))

        else:
            """ Build observer """
            if self.units(ROBOTICSFACILITY).ready.exists:
                for rf in self.units(ROBOTICSFACILITY).ready.noqueue:
                    if self.can_afford(OBSERVER) and self.supply_left > 0:
                        await self.do(rf.train(OBSERVER))
                        break
            elif self.planner.exists_plan_for(OBSERVER):
                await self.planner.advance(OBSERVER)
            else:
                self.planner.generate_new_plan(OBSERVER)

            


    async def expand(self):
        if self.units(NEXUS).amount < 3 and self.can_afford(NEXUS):
            await self.expand_now()

    async def advance_tech(self):
        if self.units(PYLON).ready.exists:
            pylon = self.units(PYLON).ready.random
            if self.units(GATEWAY).ready.exists and not self.units(CYBERNETICSCORE).exists:
                if self.can_afford(CYBERNETICSCORE) and not self.already_pending(CYBERNETICSCORE):
                    await self.build(CYBERNETICSCORE, near=pylon)
            elif len(self.units(GATEWAY)) < self.current_minute:
                if self.can_afford(GATEWAY) and not self.already_pending(GATEWAY):
                    await self.build(GATEWAY, near=pylon)

            if self.units(CYBERNETICSCORE).ready.exists:
                if self.current_minute > 3 and self.units(STARGATE).amount < 2:
                    if self.can_afford(STARGATE) and not self.already_pending(STARGATE):
                        await self.build(STARGATE, near=pylon)

    async def research_upgrades(self):
        
        if self.units(CYBERNETICSCORE).ready.exists and self.can_afford(RESEARCH_WARPGATE) and RESEARCH_WARPGATE not in self.performed_actions:
            #print(dir(self.units(CYBERNETICSCORE)[0]))
            cybercore = self.units(CYBERNETICSCORE).ready.first
            await self.do(cybercore(RESEARCH_WARPGATE))        
            self.performed_actions.add(RESEARCH_WARPGATE)        


    async def build_army(self):
        for gateway in self.units(GATEWAY).ready.noqueue:
            if not self.units(STALKER).amount > self.units(VOIDRAY).amount:
                if self.units(CYBERNETICSCORE).ready.exists and self.can_afford(STALKER) and self.supply_left > 2:
                    if random.uniform(0, 1) > 0.8:
                        await self.do(gateway.train(SENTRY))
                    else:
                        await self.do(gateway.train(STALKER))
                
        for stargate in self.units(STARGATE).ready.noqueue:
            if self.can_afford(VOIDRAY) and self.supply_left > 3:
                await self.do(stargate.train(VOIDRAY))

    async def warp_army(self, pylon=None):
        if not pylon and self.units(PYLON):
            pylon = random.choice(self.units(PYLON))
        for warpgate in self.units(WARPGATE).ready:
            can_warp = await self.get_available_abilities(warpgate)
            if AbilityId.WARPGATETRAIN_STALKER in can_warp:
                warp_location = pylon.position.to2.random_on_distance(4)
                placement = await self.find_placement(AbilityId.WARPGATETRAIN_STALKER, warp_location, placement_step=1)
                if placement is None:
                    print("could not warp")
                    return
                await self.do(warpgate.warp_in(STALKER, placement))    


    # METHOD
    def find_target(self, state):
        if len(self.known_enemy_units) > 0:
            return random.choice(self.known_enemy_units)
        elif len(self.known_enemy_structures) > 0:
            return random.choice(self.known_enemy_structures)
        else:
            return self.enemy_start_locations[0]

    async def full_attack(self, army):
        for UNIT_TYPE in army:
            UNITS = self.units(UNIT_TYPE)
            for UNIT in UNITS:
                await self.do(UNIT.attack(self.find_target(self.state)))

    async def attack(self):
        # {UNIT : [n to attack, n to defend]}
        army = {STALKER : [15, 1],
                VOIDRAY : [8, 1]}

        for UNIT in army:
            if self.units(UNIT).amount > army[UNIT][0]:
                #for s in self.units(UNIT).idle:
                #    await self.do(s.attack(self.find_target(self.state)))
                await self.full_attack(army)
            elif self.units(UNIT).amount > army[UNIT][1]:
                if len(self.known_enemy_units) > 0:
                    for s in self.units(UNIT).idle:
                        await self.do(s.attack(random.choice(self.known_enemy_units)))

#        if self.units(STALKER).amount > 15:
#            for s in self.units(STALKER).idle:
#                await self.do(s.attack(self.find_target(self.state)))
#        elif self.units(STALKER).amount > 3:
#            if len(self.known_enemy_units) > 0:
#                for s in self.units(STALKER).idle:
#                    await self.do(s.attack(random.choice(self.known_enemy_units)))



if __name__ == "__main__":
    run_game(maps.get("AbyssalReefLE"),
            [Bot(Race.Protoss, AlphaStar()), Computer(Race.Terran, Difficulty.Easy)],
            realtime=False)
