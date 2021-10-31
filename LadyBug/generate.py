import glob
import os

from tqdm import tqdm
from PIL import Image
import random
import json
from collections import defaultdict

simple_backgrounds = {
    "PurpleBlue": 1,
    "RedBlue": 1,
    "YellowGreen": 1,
    "RedPink": 1,
    "BlueBlack": 1,
}

unique_backgrounds = {
    "Monitor": 1,
    "Fire": 1,
    "SpiderWeb": 1,
    "Stick": 1,
    "Leaf": 1,
    "Hearts": 1,
    "Book": 1,
    "Matrix": 1,
    "Rainbow1": 1,
    # "Rainbow2": 1,
    # "Rainbow3": 1,
}
backgrounds = {}
backgrounds.update(simple_backgrounds)
backgrounds.update(unique_backgrounds)

bugs = {
    "Small": 1,
}

smallSpots = {
    'None': 1,
    "SmallBlackSpotsA": 1,
    "SmallBlackSpotsB": 1,
    "SmallBlackSpotsC": 1,
    "SmallRedSpotsA": 1,
    "SmallRedSpotsB": 1,
    "SmallRedSpotsC": 1,
    "SmallYellowSpotsA": 1,
    "SmallYellowSpotsB": 1,
    "SmallYellowSpotsC": 1,
}
smallColors = {
    "SmallRed": 1,
    "SmallBlue": 1,
    "SmallBlack": 1,
    "SmallGreen": 1,
    "SmallINFlag": 1,
    "SmallYellow": 1,
    "SmallOrange": 1,
    "SmallPurple": 1,
    "SmallCamo": 1,
}

accessories = {
    "None": 1,
    "Sombrero": 1,
    "TopHat": 1,
    "Turban": 1,
    "Crown": 1,
    "Construction": 1,
    "Graduation": 1,
    "Beanie": 1,
    "ChefCap": 1,
}

eyes = {
    "BlueEyes": 1,
    "RedEyes": 1,
    "WhiteEyes": 1,
    "GreyEyes": 1,
}

TO_GENERATE = 11111

TOTAL_BUGS = (
        len(backgrounds)
        * len(bugs)
        * len(smallSpots)
        * len(smallColors)
        * len(accessories)
        * len(eyes)
)


def get_ignored_combinations():
    small_spots_without_none = list(smallSpots.keys())
    small_spots_without_none.remove('None')

    accessories_without_none = list(accessories.keys())
    accessories_without_none.remove('None')

    ignore_combinations = [
        {'Spots': ['SmallYellowSpotsA', 'SmallYellowSpotsB', 'SmallYellowSpotsC'],
         'Color': ['SmallYellow', 'SmallOrange']},
        {'Spots': ['SmallRedSpotsA', 'SmallRedSpotsB', 'SmallRedSpotsC'], 'Color': ['SmallRed']},
        {'Color': ['SmallGreen'], 'Background': ['Matrix', 'Leaf']},
        {'Color': ['SmallINFlag'], 'Background': list(unique_backgrounds.keys())},
        {'Color': ['SmallINFlag'], 'Spots': small_spots_without_none},
        {'Color': ['SmallINFlag'], 'Accessory': accessories_without_none},
        {'Accessory': accessories_without_none,
         'Background': list(unique_backgrounds.keys())},
    ]

    return ignore_combinations


currentlocation = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
outputlocation = os.path.join(currentlocation, './output/')


def get_trait_key(trait):
    trait_key = ''
    for key, value in trait.items():
        trait_key = '{},{}:{}'.format(trait_key, key, value)
    return trait_key


def createCombo():
    trait = {
        "Background": random.choices(list(backgrounds.keys()), list(backgrounds.values()))[0],
        "Bug": random.choices(list(bugs.keys()), list(bugs.values()))[0],
        "Spots": random.choices(list(smallSpots.keys()), list(smallSpots.values()))[0],
        "Color": random.choices(list(smallColors.keys()), list(smallColors.values()))[0],
        "Accessory": random.choices(list(accessories.keys()), list(accessories.values()))[0],
        "Eyes": random.choices(list(eyes.keys()), list(eyes.values()))[0],
    }

    return trait


def allUnique(x):
    seen = list()
    return not any(i in seen or seen.append(i) for i in x)


def generateCombinations():
    traits = []
    trait_keys = set()
    for i in tqdm(
            iterable=range(TOTAL_BUGS),
            desc="Generating all combinations: {}".format(TOTAL_BUGS),
            total=TOTAL_BUGS,
            unit="combos",
    ):
        trait = createCombo()
        trait_key = get_trait_key(trait)

        while trait_key in trait_keys:
            trait = createCombo()
            trait_key = get_trait_key(trait)

        trait_keys.add(trait_key)
        traits.append(trait)

    return traits


def shouldIgnore(trait):
    for toIgnore in get_ignored_combinations():
        count = 0

        for key, value in trait.items():
            if value in toIgnore.get(key, []):
                count += 1

        if count > 1:
            return True

    if trait['Spots'] == 'None':
        return trait['Color'] != 'SmallINFlag'

    return False


def getImage(img):
    if "None" not in img:
        return Image.open(os.path.join(currentlocation, img)).convert('RGBA')

    return Image.new('RGBA', (24, 24), (255, 0, 0, 0))


def generate_images():
    traits = generateCombinations()

    ignored = 0
    filtered_traits = []

    for trait in tqdm(
            iterable=traits,
            desc="Filtering combinations",
            unit="combos",
    ):
        if shouldIgnore(trait):
            ignored += 1
            continue

        filtered_traits.append(trait)

    filtered_traits = random.sample(filtered_traits, k=min(TO_GENERATE, len(filtered_traits)))

    # Sort for evaluation
    filtered_traits = sorted(filtered_traits,
                             key=lambda t: (t['Background'], t['Color'], t['Spots'], t['Accessory'], t['Eyes']))

    # GET TRAIT COUNTS

    background_counts = defaultdict(int)
    bug_counts = defaultdict(int)
    spots_counts = defaultdict(int)
    color_counts = defaultdict(int)
    accessory_count = defaultdict(int)
    eyes_count = defaultdict(int)

    for trait in filtered_traits:
        background_counts[trait["Background"]] += 1
        bug_counts[trait["Bug"]] += 1
        spots_counts[trait["Spots"]] += 1
        color_counts[trait["Color"]] += 1
        accessory_count[trait["Accessory"]] += 1
        eyes_count[trait["Eyes"]] += 1

    print("ignored: ", ignored)
    print("total generated", len(filtered_traits))
    print("background:", background_counts)
    print("bugs:", bug_counts)
    print("spots:", spots_counts)
    print("colors:", color_counts)
    print("accessory:", accessory_count)
    print("eyes:", eyes_count)

    # WRITE METADATA TO JSON FILE
    with open('traits.json', 'w') as outfile:
        json.dump(filtered_traits, outfile, indent=4)

    files = glob.glob(outputlocation + "*")
    for f in files:
        os.remove(f)

    # ADD TOKEN IDS TO JSON
    i = 0
    for trait in filtered_traits:
        trait["tokenId"] = i
        i = i + 1

    # IMAGE GENERATION
    for trait in tqdm(
            iterable=filtered_traits,
            desc="Generating {} images".format(len(filtered_traits)),
            unit="images",
            total=len(filtered_traits),
    ):
        im1 = getImage(f'./Backgrounds/{trait["Background"]}.png')
        im2 = getImage(f'./Bugs/{trait["Bug"]}.png')
        im3 = getImage(f'./Colors/{trait["Color"]}.png')
        im4 = getImage(f'./Spots/{trait["Spots"]}.png')
        im5 = getImage(f'./Accessories/{trait["Accessory"]}.png')
        im6 = getImage(f'./Eyes/{trait["Eyes"]}.png')

        com1 = Image.alpha_composite(im1, im2)
        com2 = Image.alpha_composite(com1, im3)
        com3 = Image.alpha_composite(com2, im4)
        com4 = Image.alpha_composite(com3, im5)
        com5 = Image.alpha_composite(com4, im6)

        # Convert to RGB
        rgb_im = com5.convert('RGBA')

        file_name = str(trait["tokenId"]) + ".png"
        rgb_im.save(outputlocation + file_name)

    return len(filtered_traits)
