import glob
import os

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
}

bugs = {
    "Small": 1,
}

smallSpots = {
    # "SmallBlackSpotsA": 1,
    "SmallBlackSpotsB": 1,
    # "SmallBlackSpotsC": 1,
    # "SmallDarkRedSpotsA": 1,
    "SmallDarkRedSpotsB": 1,
    # "SmallDarkRedSpotsC": 1,
    # "SmallYellowSpotsA": 1,
    "SmallYellowSpotsB": 1,
    # "SmallYellowSpotsC": 1,
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
    "Sombrero": 1,
    "TopHat": 1,
    "Turban": 1,
}

eyes = {
    "BlueEyes": 1,
    "RedEyes": 1,
    "WhiteEyes": 1,
}

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
    ('SmallGreen', 'Matrix', 'Leaf'),
    ('Sombrero', 'SmallINFlag')
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

    for i in range(TOTAL_BUGS):
        trait = createCombo()
        while trait in traits:
            trait = createCombo()

        traits.append(trait)

    # Sort for evaluation
    # traits = sorted(traits, key=lambda t: (t['Background'], t['Color'], t['Spots'], t['Accessory'], t['Eyes']))

    return traits


def shouldIgnore(trait):
    count = 0
    for toIgnore in ignoreCombinations:
        for key, value in trait.items():
            if value in toIgnore:
                count += 1

    if count > 1:
        return True

    return False

def getImage(img):
    return Image.open(os.path.join(currentlocation, img)).convert('RGBA')

def generateImages():
    traits = generateCombinations()

    # GET TRAIT COUNTS

    backgroundcounts = defaultdict(int)
    bugcounts = defaultdict(int)
    spotscounts = defaultdict(int)
    colorcounts = defaultdict(int)
    accessorycount = defaultdict(int)
    eyescount = defaultdict(int)

    filteredTraits = []

    ignored = 0
    for trait in traits:
        if shouldIgnore(trait):
            ignored += 1
            continue

        backgroundcounts[trait["Background"]] += 1
        bugcounts[trait["Bug"]] += 1
        spotscounts[trait["Spots"]] += 1
        colorcounts[trait["Color"]] += 1
        accessorycount[trait["Accessory"]] += 1
        eyescount[trait["Eyes"]] += 1

        filteredTraits.append(trait)

    print("TOTAL", TOTAL_BUGS)

    print("ignored: ", ignored)
    print("background:", backgroundcounts)
    print("bugs:", bugcounts)
    print("spots:", spotscounts)
    print("colors:", colorcounts)
    print("accessory:", accessorycount)
    print("eyes:", eyescount)

    # WRITE METADATA TO JSON FILE
    with open('traits.json', 'w') as outfile:
        json.dump(filteredTraits, outfile, indent=4)

    files = glob.glob('./output/*')
    for f in files:
        os.remove(f)

    # ADD TOKEN IDS TO JSON
    i = 0
    for item in filteredTraits:
        item["tokenId"] = i
        i = i + 1

    # IMAGE GENERATION
    for item in filteredTraits:
        im1 = getImage(f'./Backgrounds/{item["Background"]}.png')
        im2 = getImage(f'./Bugs/{item["Bug"]}.png')
        im3 = getImage(f'./Colors/{item["Color"]}.png')
        im4 = getImage(f'./Spots/{item["Spots"]}.png')
        im5 = getImage(f'./Accessories/{item["Accessory"]}.png')
        im6 = getImage(f'./Eyes/{item["Eyes"]}.png')

        com1 = Image.alpha_composite(im1, im2)
        com2 = Image.alpha_composite(com1, im3)
        com3 = Image.alpha_composite(com2, im4)
        com4 = Image.alpha_composite(com3, im5)
        com5 = Image.alpha_composite(com4, im6)

        # Convert to RGB
        rgb_im = com5.convert('RGBA')

        file_name = str(item["tokenId"]) + ".png"
        rgb_im.save(outputlocation+file_name)
        # print(f'{str(item["tokenId"])} done')

    return len(filteredTraits)
