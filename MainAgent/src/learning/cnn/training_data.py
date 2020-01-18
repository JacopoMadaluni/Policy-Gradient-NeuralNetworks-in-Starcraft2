class Trainer:

    def __init__(self):
        self.attack_training_data = []


    def add_attack_data_snapshot(self, visual_data, choice):
        self.attack_training_data.append([choice, visual_data])    