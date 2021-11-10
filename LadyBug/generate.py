import glob
import os

from tqdm import tqdm
from PIL import Image
import random
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
    "Stick": 2,
    "Leaf": 2,
    "Hearts": 2,
    "Book": 2,
    "Matrix": 3,
    "Rainbow1": 3,
    "Brickwall": 4,
    "Road": 3,
    "Beach": 5,
    "Sunset": 4,
    "City": 4,

    # "Rainbow2": 1,
    # "Rainbow3": 1,

    # Cricket
    # Football
    # Basketball
    # Soccer
}

backgrounds = {}
backgrounds.update(simple_backgrounds)
backgrounds.update(unique_backgrounds)

bugs = {
    "Small": 1,
}

smallSpots = {
    'NoneSpots': 1,
    "SmallBlackSpotsA": 0.5,
    "SmallBlackSpotsB": 1,
    "SmallRedSpotsA": 0.5,
    "SmallRedSpotsB": 1,
    "SmallYellowSpotsA": 0.5,
    "SmallYellowSpotsB": 1,

    # "SmallBlackSpotsC": 0.25,
    # "SmallRedSpotsC": 0.25,
    # "SmallYellowSpotsC": 0.25,
}
smallColors = {
    "SmallRed": 1,
    "SmallBlue": 1,
    "SmallBlack": 1,
    "SmallGreen": 1,
    "SmallYellow": 1,
    "SmallOrange": 1,
    "SmallPurple": 1,
    "SmallCamo": 1,

    # "SmallINFlag": 1,
}

accessories = {
    "NoneAccessory": 2,
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
    "Cloak": 0.25,
    "SnorkelGear": 1,
    "RedSunGlasses": 0.25,
    "GreySunGlasses": 0.25,
}

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

currentlocation = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
outputlocation = os.path.join(currentlocation, './output/')

backgrounds_with_accessories = {
    'Beach': ['RedSunGlasses', 'GreySunGlasses', 'Bikini', 'BeachHat', 'PirateHat'],
    'Book': ['Graduation'],
    'Brickwall': ['Construction'],
    'City': ['Tux'],
    'Clouds': ['RedSunGlasses', 'GreySunGlasses'],
    'Fire': ['Cloak'],
    'SpiderWeb': ['WizardHat'],
    'Sunset': ['GreySunGlasses'],
    'Wave': ['RedSunGlasses', 'GreySunGlasses', 'Bikini', 'BeachHat', 'PirateHat'],
}


def is_combo(trait):
    return trait['Background'] in backgrounds_with_accessories and trait['Accessory'] in backgrounds_with_accessories[
        trait['Background']]


def get_combo_key(trait):
    return '{}:{}'.format(trait['Background'], trait['Accessory'])


def allowed_accessories_as_ignore_combination(background, allowed):
    aa = [a for a in allowed]
    aa.append('NoneAccessory')

    return {
        'Background': [background],
        'Accessory': set([a for a in list(accessories.keys()) if a not in aa])
    }


def get_ignored_combinations():
    small_spots_without_none = list(smallSpots.keys())
    small_spots_without_none.remove('NoneSpots')

    accessories_without_none = list(accessories.keys())
    accessories_without_none.remove('NoneAccessory')

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

        # Ignore red sunglasses with red bug
        {"Accessory": ["RedSunGlasses"], "Color": ["SmallRed"]},

        # Ignore grey sunglasses with red bug
        {"Accessory": ["GreySunGlasses"], "Color": ["SmallBlack"]},

        # Ignore graduation cap with black color bug
        {"Accessory": ["Graduation"], "Color": ["SmallBlack"]}

    ]

    for bg in unique_backgrounds:
        if bg in backgrounds_with_accessories:
            ignore_combinations.append(allowed_accessories_as_ignore_combination(bg, backgrounds_with_accessories[bg]))
        else:
            ignore_combinations.append({'Background': [bg], 'Accessory': set(accessories_without_none)})

    return ignore_combinations


ignored_combinations = get_ignored_combinations()


def shouldIgnore(trait):
    for toIgnore in ignored_combinations:
        count = 0

        for key, value in trait.items():
            if value in toIgnore.get(key, set()):
                count += 1

        if count > 1:
            return True

    if trait['Spots'] == 'NoneSpots':

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
        trait['Background'] = 'NoneBackground'

    elif trait['Accessory'] == 'Tux':
        trait['Color'] = 'NoneColor'
        trait['Spots'] = 'NoneSpots'

    elif trait['Accessory'] == 'BathRobe':
        trait['Spots'] = 'NoneAccessory'

    elif trait["Accessory"] in ("RedSunGlasses", "GreySunGlasses", "SnorkelGear"):
        trait["Eyes"] = 'NoneEyes'

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
    trait_keys = set()

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


def generate_images(traits):
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

        rgb_im = rgb_im.resize((120, 120), Image.NEAREST)

        file_name = str(trait["tokenId"]) + ".png"
        rgb_im.save(outputlocation + file_name)

    return traits


def post_process(traits):
    for trait in tqdm(
            iterable=traits,
            desc="Postprocessing {} traits".format(len(traits)),
            unit="traits",
            total=len(traits),
    ):
        if trait['Accessory'] == 'Bedroom':
            trait['Background'] = 'Bedroom'
            trait['Accessory'] = 'NoneAccessory'

        if is_combo(trait):
            combo_to_severity = {
                'Wave:BeachHat': 'Minor',
                'Beach:BeachHat': 'Minor',
                'City:Tux': 'Blocker',
                'Beach:PirateHat': 'Trivial',
                'Wave:GreySunGlasses': 'Trivial',
                'Brickwall:Construction': 'Trivial',
                'Wave:PirateHat': 'Trivial',
                'Beach:RedSunGlasses': 'Blocker',
                'SpiderWeb:WizardHat': 'Minor',
                'Fire:Cloak': 'Blocker',
                'Book:Graduation': 'Major',
                'Beach:Bikini': 'Critical',
                'Wave:Bikini': 'Major',
                'Clouds:RedSunGlasses': 'Minor',
                'Sunset:GreySunGlasses': 'Critical',
                'Beach:GreySunGlasses': 'Minor',
                'Clouds:GreySunGlasses': 'Minor',
                'Wave:RedSunGlasses': 'Minor',
            }
            combo_key = get_combo_key(trait)
            trait['Severity'] = combo_to_severity[combo_key]

        elif trait['Accessory'] in ('Tux', 'Cloak', 'Bikini') or trait['Background'] in ('Matrix', 'Fire', 'Rainbow1'):
            trait['Severity'] = 'Blocker'

        elif trait['Accessory'] in ('RedHair', 'BeachHat') or trait['Background'] in ('Sunset', 'City'):
            trait['Severity'] = 'Critical'

        elif trait['Accessory'] in ('Crown', 'VikingHelmet', 'Halo', 'TopHat') or trait['Background'] in ('Stick',):
            trait['Severity'] = 'Major'

        elif (trait['Accessory'] in ('BathRobe', 'Turban', 'PirateHat', 'Belt', 'Construction', 'ChefCap') or
              trait['Background'] in ('AmericanFootball', 'TennisBall', 'Leaf', 'Monitor', 'Hearts', 'SpiderWeb')):
            trait['Severity'] = 'Minor'
        else:
            trait['Severity'] = 'Trivial'

        for key, value in trait.items():
            if key == "tokenId":
                continue

            if "None" in value:
                trait[key] = None

            if key != "Bug" and "Small" in value:
                trait[key] = value[5:]

    for trait in traits:
        assert 'Severity' in trait
        assert trait['Severity'] in ['Blocker', 'Critical', 'Major', 'Minor', 'Trivial']

        assert 'NoneAccessory' != trait['Accessory']
        assert 'NoneBackground' != trait['Background']
        assert 'NoneColor' != trait['Color']
        assert 'NoneSpots' != trait['Spots']

    return traits


def count_traits(traits):
    # GET TRAIT COUNTS

    background_counts = defaultdict(int)
    bug_counts = defaultdict(int)
    spots_counts = defaultdict(int)
    color_counts = defaultdict(int)
    accessory_count = defaultdict(int)
    eyes_count = defaultdict(int)
    severity_count = defaultdict(int)
    combo_count = defaultdict(int)

    for trait in tqdm(
            iterable=traits,
            desc="Counting individual traits in {}".format(len(traits)),
            unit="trait",
            total=len(traits),
    ):

        bug_counts[trait["Bug"]] += 1
        spots_counts[trait["Spots"]] += 1
        color_counts[trait["Color"]] += 1
        eyes_count[trait["Eyes"]] += 1
        severity_count[trait['Severity']] += 1

        if is_combo(trait):
            combo_count[get_combo_key(trait)] += 1
        else:
            background_counts[trait["Background"]] += 1
            accessory_count[trait["Accessory"]] += 1

    print_csv(background_counts)
    print_csv(bug_counts)
    print_csv(spots_counts)
    print_csv(color_counts)
    print_csv(accessory_count)
    print_csv(eyes_count)
    print_csv(combo_count)
    print_csv(severity_count)


def print_csv(d):
    for key, value in d.items():
        print("{},{}".format(key, value))
