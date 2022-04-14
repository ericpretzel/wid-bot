import random
import config
import markovify
import os

"""
Note to Eric for later: os.path.getmtime() returns the last time a file was modified.
Could be useful for automatically updating models.
"""

def generate_demon_report(server: int, data: dict):
    """
    Generates a demon report for a server.

    server (int) - the ID of the server.
    data (dict)  - Maps user ID to a list of the content of all the messages they have sent

    Data is stored like this:

    -demons
        -server#1
            -user#1.json \\
            -user#2.json
        -server#2
            -user#1.json \\
            -user#2.json
        -server#3
            -user#1.json
    ...etc.

    This means users can have different models depending on the server it is requested from.
    """
    server_folder = os.path.join(config.DEMONS_FOLDER, str(server), )
    if not os.path.isdir(server_folder):
        os.mkdir(server_folder)
    
    for user, messages in data.items():
        corpus = '\n'.join([msg.replace('.', '\n') for msg in messages])
        model = markovify.NewlineText(corpus, well_formed=False)

        filepath = os.path.join(server_folder, str(user) + '.json')
        with open(filepath, 'w') as f:
            f.write(model.to_json())

def generate_sentences(server: int, user: int, num_sentences: int) -> str:
    """
    Loads json model from file and generates a string of (`num_sentences`) sentences.

    If the model could not be found, raises `ModelNotFoundException`.
    """
    filepath = os.path.join(config.DEMONS_FOLDER, str(server), f'{user}.json')
    if not os.path.isfile(filepath):
        raise ModelNotFoundException()
    
    with open(filepath) as f:
        model = markovify.Text.from_json(f.readline().strip())


    result = [model.make_sentence(min_words=random.randint(2, 10)) for _ in range(num_sentences)]

    return '. '.join(filter(None, result))

class ModelNotFoundException(Exception):
    pass