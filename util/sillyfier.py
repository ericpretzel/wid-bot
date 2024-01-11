import random
from collections import defaultdict

def load_silly(filename):
    phrases = defaultdict(set)
    # todo put file path in config file
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            if not line or line.startswith('//'): continue
            # this can be more memory efficient with 'pointers' but idc
            tags_str, content = line.split(':', 1)
            tags = tags_str[1:-1].split('|')
            for tag in tags:
                phrases[tag].add(content)
    return phrases

def insert_content(phrases: defaultdict[str, set], sentence: str, depth=0):
    # replaces the tags with corresponding phrases
    # look for tags such as [NOUN], then insert a random phrase with the same tag.
    # also call this function recursively on that phrase.
    if depth > 5: return sentence
    while True:
        if depth == 0: print(sentence)
        try:
            start = sentence.index('[')
            end = sentence.index(']', start + 1)
        except ValueError: # we have no more phrases to insert
            return sentence
        tags = sentence[start+1:end].split('|')
        all_phrases = set()
        for tag in tags:
            all_phrases |= phrases[tag]
        phrase = insert_content(random.choice(tuple(all_phrases)), depth + 1)

        sentence = sentence[:start] + phrase + sentence[end+1:]

def sillyfy(phrases: defaultdict[str, set]):
    sentence: str = random.choice(tuple(phrases['SENTENCE']))
    return insert_content(sentence)
