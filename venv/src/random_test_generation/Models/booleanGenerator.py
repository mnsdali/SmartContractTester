import random

class BooleanGenerator:
    
    def boolGenerator(self):
        b = random.choice([True, False])
        return "true" if b else "false"