import json

from upload_to_pinata import upload_to_pinata
from combine import combine
from generate import (
    generate_images,
    generateCombinations,
    post_process,
    count_traits,
    allUnique,
    get_trait_key,
)

ONLY_UPLOAD_TO_PINATA = False

if __name__ == "__main__":

    if not ONLY_UPLOAD_TO_PINATA:

        traits = generateCombinations()

        traits = generate_images(traits)

        traits = post_process(traits)

        assert allUnique([get_trait_key(trait) for trait in traits])

        combine(traits)

        count_traits(traits)

        with open('traits.json', 'w') as outfile:
            json.dump(traits, outfile, indent=4)

    else:

        traits = upload_to_pinata('traits.json')

        with open('../database/traitsfinal.json', 'w') as outfile:
            json.dump(traits, outfile, indent=4)

    print("done")
