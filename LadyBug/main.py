import json

from combine import combine
from generate import (
    generate_images,
    generateCombinations,
    post_process,
    count_traits,
    allUnique,
    get_trait_key,
)

traits = generateCombinations()

traits = generate_images(traits)

traits = post_process(traits)

assert allUnique([get_trait_key(trait) for trait in traits])

with open('traits.json', 'w') as outfile:
    json.dump(traits, outfile, indent=4)

count_traits(traits)

combine(traits)

print("done")
