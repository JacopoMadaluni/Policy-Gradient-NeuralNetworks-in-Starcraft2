from info import protoss_units

class ArmyCompModel:

    def __init__(self, enemy_units):
        self.enemy_units = enemy_units
        print("------")
        print(enemy_units)
        print("------")

        self.enemy_unit_types = []
        self.init_enemy_unit_types()

        self.protoss_units = protoss_units()

        self.units = []
        self.init_protoss_units_by_utility()

    def init_enemy_unit_types(self):
        for e in self.enemy_units:
            self.enemy_unit_types.append(e[0])

    def sort_append(self, unit, utility):
        if len(self.units) == 0:
            self.units.append([unit, utility])
        else:
            for i, e in enumerate(self.units):
                if e[1] < utility:
                    self.units.insert(i, [unit, utility])
                    return

        # nothing was appended
        self.units.append([unit, utility])



    def compute_utility(self, unit):
        utility = 0
        for e in self.enemy_units:
            u      = e[0]
            amount = e[1]
            utility += self.protoss_units[unit]["utility_against"][u] * amount
        return utility

    def init_protoss_units_by_utility(self):
        for unit in self.protoss_units:
            self.sort_append(unit, self.compute_utility(unit))

        self.normalize_utilities()

    def normalize_utilities(self):
        total = 0
        for e in self.units:
            total += e[1]

        if total == 0:
            total = 1
            
        for e in self.units:
            e[1] = e[1]/total

    def percentage_of(self, unit):
        """
        To be implemented
        """
        return ""

    def normalize_percentages(self, composition):
        """
        Yet another one to be implemented
        """
        return ""

    def utility_of(self, unit_tag):
        for e in self.units:
            if e[0] == unit_tag:
                return e[1]
        return None

    def army_comp(self):
        countered_units = set()
        table = protoss_units()
        composition = []
        for unit in self.units:
            counters = table[unit]["counters"]
            percentage = 0
            for c in counters:
                if c not in countered_units and c in self.enemy_units:
                    countered_units.add(c)
                    percentage_of_c = self.percentage_of(c)
                    percentage += percentage_of_c
            composition.append((unit, percentage))

            # break condition if we countered all enemy units
            if len(countered_units) == len(self.enemy_units):
                break

        return self.normalize_percentages(composition)
