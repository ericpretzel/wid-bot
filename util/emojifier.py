import json
import random
import re

class Emojifier:
    def __init__(self, mappings: dict):
        self.mappings = mappings

    def emojify(self, txt: str):
        ret = ''

        # add whitespace to the end of txt 
        # so we don't miss the last non-whitespace token
        txt += ' '
        
        whitespaces = [match.group(0) for match in re.finditer(r'\s+', txt)]
        words = re.split(r'\s+', txt)

        for word, whitespace in zip(words, whitespaces):
            ret += word
            try:
                key = re.split(r'\W', word)[0].lower()
                emojis = self.mappings[key]
            except KeyError:
                emojis = random.choice(tuple(self.mappings.values()))

            chance = 0.75
            for _ in range(3):
                if random.random() >= 1.0 - chance:
                    ret += ' ' + random.choice(emojis)
                    chance -= 0.25
            ret += whitespace
        return ret
    
    # add other functions to make this class more robust?
