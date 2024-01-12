import random
import io
from collections import defaultdict
import json
import config
import os
from PIL import Image, ImageFont, ImageDraw
import textwrap

def load_silly(folder_path):
    image_data_file = os.path.join(folder_path, 'images.json')
    with open(image_data_file) as f:
        image_data = json.load(f)

    content_file = os.path.join(folder_path, 'content.lob')
    phrases = defaultdict(set)
    with open(content_file) as f:
        for line in f.readlines():
            line = line.strip()
            if not line or line.startswith('//'): continue
            # this can be more memory efficient with 'pointers' but idc
            tags_str, content = line.split(':', 1)
            tags = tags_str[1:-1].split('|')
            for tag in tags:
                phrases[tag].add(content)
    return phrases, image_data

def insert_content(phrases: defaultdict[str, set], sentence: str, depth=0):
    # replaces the tags with corresponding phrases
    # look for tags such as [NOUN], then insert a random phrase with the same tag.
    # also call this function recursively on that phrase.
    if depth > 5: return sentence
    while True:
        try:
            start = sentence.index('[')
            end = sentence.index(']', start + 1)
        except ValueError: # we have no more phrases to insert
            return sentence
        tags = sentence[start+1:end].split('|')
        all_phrases = set()
        for tag in tags:
            all_phrases |= phrases[tag]
        phrase = insert_content(phrases, random.choice(tuple(all_phrases)), depth + 1)

        sentence = sentence[:start] + phrase + sentence[end+1:]

def sillyfy(phrases: defaultdict[str, set]):
    sentence: str = random.choice(tuple(phrases['SENTENCE']))
    return insert_content(phrases, sentence)

def generate_image(phrases: defaultdict[str, set], image_data: dict, num_images=1) -> io.BytesIO:
    # todo stitch multiple images together? make it a parameter?

    image_name = random.choice(tuple(image_data.keys()))
    img = Image.open(image_name)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(config.FONT_COMIC_SANS, 64)

    rectangles = image_data[image_name]
    sentences = [sillyfy(phrases) for _ in range(len(rectangles))]
    for rect, sentence in zip(rectangles, sentences):
        x = rect['x']
        y = rect['y']
        w = rect['w']
        h = rect['h']

        font.size = img.width * img.height * 0.05

        text = '\n'.join(textwrap.wrap(sentence, rect['w'] // 36)).upper()

        draw.rectangle((x, y, x + w, y + h), fill=(255, 255, 255))
        draw.text((x, y), text, (0,0,0), font=font)

    buf = io.BytesIO()
    img.save(buf, 'png')
    buf.seek(0)
    return buf
