import glob
import os

from tqdm import tqdm
from PIL import Image
import random
import json
from collections import defaultdict

TO_GENERATE = 11111

# add up to or 100,
simple_backgrounds = {
    "PurpleBlue": 5,
    "RedBlue": 5,
    "YellowGreen": 5,
    "RedPink": 5,
    "BlueBlack": 5,
}

unique_backgrounds = {
    "AmericanFootball": 1,
    "TennisBalls": 1,
    "Monitor": 2,
    "Fire": 5,
    "Clouds": 5,
    "Wave": 5,
    "SpiderWeb": 2,
    "Stick": 5,
    "Leaf": 3,
    "Hearts": 2,
    "Book": 2,
    "Matrix": 3,
    "Rainbow1": 4,
    "Rainbow2": 1,
    "Brickwall": 3,
    "Road": 3,

    # "Rainbow3": 1,
    # Cricket
    # Football
    # Basketball
    # Soccer
    # Brick Wall
}

backgrounds = {}
backgrounds.update(simple_backgrounds)
backgrounds.update(unique_backgrounds)

total_background_weight = sum(backgrounds.values())
probs = []

for bg, w in backgrounds.items():
    p = (w / (total_background_weight * 1.0))
    probs.append(p)
    print('{}: {}, {}'.format(bg, p, p * TO_GENERATE))

print(sum(probs))

bugs = {
    "Small": 1,
}

smallSpots = {
    'None': 1,
    "SmallBlackSpotsA": 0.5,
    "SmallBlackSpotsB": 1,
    # "SmallBlackSpotsC": 0.25,
    "SmallRedSpotsA": 0.5,
    "SmallRedSpotsB": 1,
    # "SmallRedSpotsC": 0.25,
    "SmallYellowSpotsA": 0.5,
    "SmallYellowSpotsB": 1,
    # "SmallYellowSpotsC": 0.25,
}
smallColors = {
    "SmallRed": 1,
    "SmallBlue": 1,
    "SmallBlack": 1,
    "SmallGreen": 1,
    # "SmallINFlag": 1,
    "SmallYellow": 1,
    "SmallOrange": 1,
    "SmallPurple": 1,
    "SmallCamo": 1,
}

accessories = {
    "None": 2,
    "Sombrero": 3,
    "TopHat": 3,
    "Turban": 1,  # Rare
    "Crown": 3,
    "Construction": 2,
    "Graduation": 2,
    "Beanie": 1,
    "ChefCap": 3,
    "Bikini": 2,
    "VikingHelmet": 3,
    "Belt": 2,
    "WizardHat": 3,
    "BeachHat": 3,
    "Bedroom": 2,
    "Halo": 3,
    "ClownHat": 3,
    "RedHair": 2,
    "PirateHat": 1.5,
    "Tux": 3,
    "BathRobe": 2,
    "Cloak": 0.5,
    "SnorkelGear": 1,
}

total_accessories_weight = sum(accessories.values())
probs = []

for a, w in accessories.items():
    p = (w / (total_accessories_weight * 1.0))
    probs.append(p)
    print('{}: {}, {}'.format(a, p, p * TO_GENERATE))

print(sum(probs))

# Sports ->

eyes = {
    "BlueEyes": 1,
    "RedEyes": 1,
    "WhiteEyes": 1,
    "GreyEyes": 0.25,
}

TOTAL_BUGS = (
        len(backgrounds)
        * len(bugs)
        * len(smallSpots)
        * len(smallColors)
        * len(accessories)
        * len(eyes)
)

trait_keys = set()

currentlocation = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
outputlocation = os.path.join(currentlocation, './output/')


def get_ignored_combinations():
    small_spots_without_none = list(smallSpots.keys())
    small_spots_without_none.remove('None')

    accessories_without_none = list(accessories.keys())
    accessories_without_none.remove('None')

    ignore_combinations = [
        # Ignore Yellow spots with Yellow or Orange colored bugs
        {'Spots': ['SmallYellowSpotsA', 'SmallYellowSpotsB', 'SmallYellowSpotsC'],
         'Color': ['SmallYellow', 'SmallOrange']},

        # Ignore Red spots with Red Colored Bugs
        {'Spots': ['SmallRedSpotsA', 'SmallRedSpotsB', 'SmallRedSpotsC'], 'Color': ['SmallRed', 'SmallPurple']},

        # Ignore Green Colored bug with Matrix or Leaf Background
        {'Color': ['SmallGreen'], 'Background': ['Matrix', 'Leaf']},

        # Ignore Flag with any unique background
        {'Color': ['SmallINFlag'], 'Background': list(unique_backgrounds.keys())},

        # Ignore Flag with all spots
        {'Color': ['SmallINFlag'], 'Spots': small_spots_without_none},

        # Ignore Flag with all accessories
        {'Color': ['SmallINFlag'], 'Accessory': accessories_without_none},

        # Ignore all combinations of accessories and unique backgrounds
        {'Accessory': accessories_without_none, 'Background': list(unique_backgrounds.keys())},

        # Ignore bikini accessory with red spots
        {"Accessory": ['Bikini'], 'Spots': ['SmallRedSpotsA', 'SmallRedSpotsB', 'SmallRedSpotsC']},

        # Ignore cloak with redpink background
        {"Accessory": ["Cloak"], 'Background': ['RedPink']},

        # Ignore bikini accessory with red or purple colored bugs
        {"Accessory": ['Bikini'], 'Color': ['SmallRed', 'SmallPurple']},

        # Ignore Wizard hat accessory with blueblack or redblue backgrounds
        {"Accessory": ["WizardHat"], "Background": ['BlueBlack', 'RedBlue']},

        # Ignore pirate hat and cloak  accessory with purpleblue background
        {"Accessory": ["PirateHat", "Cloak"], "Background": ['PurpleBlue']},

        # Ignore snorkel gear with orange color bug
        {"Accessory": ["SnorkelGear"], "Color": ["SmallOrange"]},

        # Ignore snorkel gear with grey eyes
        {"Accessory": ["SnorkelGear"], "Eyes": ["GreyEyes"]},
    ]

    return ignore_combinations


def shouldIgnore(trait):
    for toIgnore in get_ignored_combinations():
        count = 0

        for key, value in trait.items():
            if value in toIgnore.get(key, []):
                count += 1

        if count > 1:
            return True

    if trait['Spots'] == 'None':

        # None spots can go with Flag
        if trait['Color'] == 'SmallINFlag':
            return False

        # None spots cannot go with anything Tux or BathRobe
        if trait['Accessory'] not in ('Tux', 'BathRobe'):
            return True

    return False


def createCombo():
    trait = {
        "Background": random.choices(list(backgrounds.keys()), list(backgrounds.values()))[0],
        "Bug": random.choices(list(bugs.keys()), list(bugs.values()))[0],
        "Spots": random.choices(list(smallSpots.keys()), list(smallSpots.values()))[0],
        "Color": random.choices(list(smallColors.keys()), list(smallColors.values()))[0],
        "Accessory": random.choices(list(accessories.keys()), list(accessories.values()))[0],
        "Eyes": random.choices(list(eyes.keys()), list(eyes.values()))[0],
    }

    if trait['Accessory'] == 'Bedroom':
        trait['Background'] = 'None'

    elif trait['Accessory'] == 'Tux':
        trait['Color'] = 'None'
        trait['Spots'] = 'None'

    elif trait['Accessory'] == 'BathRobe':
        trait['Spots'] = 'None'

    return trait


def get_trait_key(trait):
    trait_key = ''
    for key, value in trait.items():
        trait_key = '{},{}:{}'.format(trait_key, key, value)
    return trait_key


def allUnique(x):
    seen = list()
    return not any(i in seen or seen.append(i) for i in x)


def generateCombinations():
    traits = []
    for i in tqdm(
            iterable=range(TO_GENERATE),
            desc="Generating {} combinations".format(TO_GENERATE),
            total=TO_GENERATE,
            unit="combos",
    ):
        trait = createCombo()
        trait_key = get_trait_key(trait)

        while trait_key in trait_keys or shouldIgnore(trait):
            trait = createCombo()
            trait_key = get_trait_key(trait)

        trait_keys.add(trait_key)
        traits.append(trait)

    return traits


def getImage(img):
    if "None" not in img:
        return Image.open(os.path.join(currentlocation, img)).convert('RGBA')

    return Image.new('RGBA', (24, 24), (255, 0, 0, 0))


def generate_images():
    traits = generateCombinations()

    # Sort for evaluation
    traits = sorted(traits,
                    key=lambda t: (t['Background'], t['Color'], t['Spots'], t['Accessory'], t['Eyes']))

    files = glob.glob(outputlocation + "*")
    for f in files:
        os.remove(f)

    # ADD TOKEN IDS TO JSON
    i = 0
    for trait in traits:
        trait["tokenId"] = i
        i = i + 1

    # IMAGE GENERATION
    for trait in tqdm(
            iterable=traits,
            desc="Generating {} images".format(len(traits)),
            unit="images",
            total=len(traits),
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

    # GET TRAIT COUNTS

    background_counts = defaultdict(int)
    bug_counts = defaultdict(int)
    spots_counts = defaultdict(int)
    color_counts = defaultdict(int)
    accessory_count = defaultdict(int)
    eyes_count = defaultdict(int)

    for trait in traits:
        if trait['Accessory'] == 'BedRoom':
            trait['Background'] = 'BedRoom'
            trait['Accessory'] = 'None'

        background_counts[trait["Background"]] += 1
        bug_counts[trait["Bug"]] += 1
        spots_counts[trait["Spots"]] += 1
        color_counts[trait["Color"]] += 1
        accessory_count[trait["Accessory"]] += 1
        eyes_count[trait["Eyes"]] += 1

    print("background:", background_counts)
    print("bugs:", bug_counts)
    print("spots:", spots_counts)
    print("colors:", color_counts)
    print("accessory:", accessory_count)
    print("eyes:", eyes_count)

    # WRITE METADATA TO JSON FILE

    with open('traits.json', 'w') as outfile:
        json.dump(traits, outfile, indent=4)

    return len(traits)
