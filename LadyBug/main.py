import json

from upload_to_pinata import upload_to_pinata
from combine import combine, combineToGif
from generate import (
    generate_images,
    generateCombinations,
    count_traits,
    allUnique,
    get_trait_key,
    print_csv,
)

from rarity import generate_bar_graph_from_counts, calculate_scores, generate_histogram_from_scores

TO_GENERATE = 11111

ONLY_UPLOAD_TO_PINATA = False

EXCLUDE_TRAITS_IN_FILE = ''

if __name__ == "__main__":

    if not ONLY_UPLOAD_TO_PINATA:

        excluded_traits = []
        if EXCLUDE_TRAITS_IN_FILE != '':
            with open(EXCLUDE_TRAITS_IN_FILE) as f:
                excluded_traits = json.load(f)

        traits = generateCombinations(TO_GENERATE, excluded_traits=excluded_traits)

        traits = generate_images(traits)

        assert allUnique([get_trait_key(trait) for trait in traits])

        for trait in traits:
            if trait['Color'] is None:
                assert trait['Accessory'] == 'Tux'

        combine(traits)

        # combineToGif(traits)

        background_counts, spots_counts, color_counts, accessory_counts, eyes_counts, combo_counts = (
            count_traits(traits)
        )

        print_csv("backgrounds", background_counts)
        print_csv("spots", spots_counts)
        print_csv("colors", color_counts)
        print_csv("accessories", accessory_counts)
        print_csv("eyes", eyes_counts)
        print_csv("combos", combo_counts)

        with open('traits.json', 'w') as outfile:
            json.dump(traits, outfile, indent=4)

        generate_bar_graph_from_counts(
            background_counts,
            spots_counts,
            color_counts,
            accessory_counts,
            eyes_counts,
            combo_counts,
        )

        trait_scores = calculate_scores(
            background_counts,
            spots_counts,
            color_counts,
            accessory_counts,
            eyes_counts,
            combo_counts,
            traits
        )

        generate_histogram_from_scores(trait_scores)

    else:

        traits = upload_to_pinata('traits.json')

        with open('../database/traitsfinal.json', 'w') as outfile:
            json.dump(traits, outfile, indent=4)

    print("done")
