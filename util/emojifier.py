import random
import re

class Emojifier:
    def __init__(self, mappings: dict):
        self.mappings = mappings

    # TODO: make whitespace consistent. 
    # Currently just replaces any newlines or multi-spaces with singular spaces
    def emojify(self, txt: str):
        ret = ''
        for word in re.split(r'\s+', txt):
            ret += word + ' '
            try:
                key = re.split(r'\W', word)[0]
                emojis = self.mappings[key]
            except KeyError: continue

            chance = 0.85
            for _ in range(3):
                if (1.0 - random.random()) >= chance:
                    ret += random.choice(emojis) + ' '
                    chance -= 0.25
        return ret
    
    # add other functions to make this class more robust?
