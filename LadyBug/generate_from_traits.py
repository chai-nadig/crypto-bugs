import json

from generate import generate_images
from combine import combine

with open('traits.json') as f:
    traits = json.load(f)

generate_images(traits)

combine(traits)
