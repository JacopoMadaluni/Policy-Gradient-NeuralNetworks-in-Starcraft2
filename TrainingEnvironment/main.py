

from mathematical_model.model import ArmyCompModel
from evaluator import army_generator


if __name__ == "__main__":
    enemy_army = army_generator.bio_army(30)
    model = ArmyCompModel(enemy_army)
    print(model.enemy_units)   
    print(model.enemy_unit_types)    
    print(model.units)       