import glob
import os

from tqdm import tqdm
from PIL import Image
import random
import json
from collections import defaultdict

backgrounds = {
    "SpiderWeb": 1,
    "Stick": 1,
    "Leaf": 1,
    "Hearts": 1,
    "Book": 1,
    "Matrix": 1,
    "Rainbow1": 1,
    "Rainbow2": 1,
    "Rainbow3": 1,
    "PurpleBlue": 1,
    "RedBlue": 1,
    "YellowGreen": 1,
    "RedPink": 1,
    "BlueBlack": 1,
}

bugs = {
    "Small": 1,
}

smallSpots = {
    "SmallBlackSpotsA": 1,
    "SmallBlackSpotsB": 1,
    "SmallBlackSpotsC": 1,
    "SmallDarkRedSpotsA": 1,
    "SmallDarkRedSpotsB": 1,
    "SmallDarkRedSpotsC": 1,
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
}

accessories = {
    "None": 1,
    "Sombrero": 1,
    "TopHat": 1,
    "Turban": 1,
    "Crown": 1,
}

eyes = {
    "BlueEyes": 1,
    "RedEyes": 1,
    "WhiteEyes": 1,
    "GreyEyes": 1,
}

TO_GENERATE = 10000

TOTAL_BUGS = (
        len(backgrounds)
        * len(bugs)
        * len(smallSpots)
        * len(smallColors)
        * len(accessories)
        * len(eyes)
)

ignoreCombinations = [
    ('SmallYellowSpotsA', 'SmallYellowSpotsB', 'SmallYellowSpotsC', 'SmallYellow'),
    ('SmallDarkRedSpotsA', 'SmallDarkRedSpotsB', 'SmallDarkRedSpotsC', 'SmallRed'),
    ('SmallGreen', 'Matrix', 'Leaf'),
    ('Sombrero', 'SmallINFlag'),
    ('Sombrero', 'TopHat', 'Turban', "Crown", "SpiderWeb", "Stick", "Leaf", "Hearts", "Book", "Matrix", "Rainbow1",
     "Rainbow2", "Rainbow3",)
]

currentlocation = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
outputlocation = os.path.join(currentlocation, '../output/')


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

    for i in tqdm(
            iterable=range(TOTAL_BUGS),
            desc="Generating all combinations: {}".format(TOTAL_BUGS),
            total=TOTAL_BUGS,
            unit="combos",
    ):
        trait = createCombo()
        while trait in traits:
            trait = createCombo()

        traits.append(trait)

    return traits


def shouldIgnore(trait):
    count = 0
    for toIgnore in ignoreCombinations:
        for key, value in trait.items():
            if value in toIgnore:
                count += 1

        if count > 1:
            return True

        count = 0

    return False


def getImage(img):
    return Image.open(os.path.join(currentlocation, img)).convert('RGBA')


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

    print("total generated", len(filtered_traits))
    print("ignored: ", ignored)
    print("background:", background_counts)
    print("bugs:", bug_counts)
    print("spots:", spots_counts)
    print("colors:", color_counts)
    print("accessory:", accessory_count)
    print("eyes:", eyes_count)

    # WRITE METADATA TO JSON FILE
    with open('traits.json', 'w') as outfile:
        json.dump(filtered_traits, outfile, indent=4)

    files = glob.glob('./output/*')
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
            desc="Generating images",
            unit="images",
    ):
        im1 = Image.open(f'./Backgrounds/{trait["Background"]}.png').convert('RGBA')
        im2 = Image.open(f'./Bugs/{trait["Bug"]}.png').convert('RGBA')
        im3 = Image.open(f'./Colors/{trait["Color"]}.png').convert('RGBA')
        im4 = Image.open(f'./Spots/{trait["Spots"]}.png').convert('RGBA')
        im5 = (
            Image.open(f'./Accessories/{trait["Accessory"]}.png').convert('RGBA')
            if trait["Accessory"] != "None" else Image.new('RGBA', (24, 24), (255, 0, 0, 0))
        )
        im6 = Image.open(f'./Eyes/{trait["Eyes"]}.png').convert('RGBA')

        com1 = Image.alpha_composite(im1, im2)
        com2 = Image.alpha_composite(com1, im3)
        com3 = Image.alpha_composite(com2, im4)
        com4 = Image.alpha_composite(com3, im5)
        com5 = Image.alpha_composite(com4, im6)

        # Convert to RGB
        rgb_im = com5.convert('RGBA')

        file_name = str(trait["tokenId"]) + ".png"
        rgb_im.save("./output/" + file_name)
        # print(f'{str(trait["tokenId"])} done')

    return len(filtered_traits)
