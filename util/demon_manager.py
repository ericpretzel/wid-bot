import random
import config
import markovify
import os

def generate_demon_report(data: dict):
    """
    Generates a demon report for a server.

    data (dict)  - Maps user ID to a list of the content of all the messages they have sent

    Stores data for each user

    """
    folder = os.path.join(config.DEMONS_FOLDER, )
    if not os.path.isdir(folder):
        os.mkdir(folder)
    
    for user, messages in data.items():
        corpus = '\n'.join([msg.replace('.', '\n') for msg in messages])
        model = markovify.NewlineText(corpus, well_formed=False)

        filepath = os.path.join(folder, str(user) + '.json')
        with open(filepath, 'w') as f:
            f.write(model.to_json())

def generate_sentences(user: int, num_sentences: int) -> str:
    """
    Loads json model from file and generates a string of (`num_sentences`) sentences.

    If the model could not be found, raises `ModelNotFoundException`.
    """
    filepath = os.path.join(config.DEMONS_FOLDER, f'{user}.json')
    if not os.path.isfile(filepath):
        raise ModelNotFoundException()
    
    with open(filepath) as f:
        model = markovify.Text.from_json(f.readline().strip())

    result = [model.make_sentence(min_words=random.randint(2, 10)) for _ in range(num_sentences)]

    return '. '.join(filter(None, result))

class ModelNotFoundException(Exception):
    pass
