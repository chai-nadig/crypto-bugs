import glob
import os

from PIL import Image
import random
from collections import defaultdict

from tqdm import tqdm

simple_backgrounds = {
    "Purple Blue": 5,
    "Red Blue": 5,
    "Yellow Green": 5,
    "Red Pink": 5,
    "Blue Black": 5,
    "Gold": 0.1,
}

unique_backgrounds = {
    "American Football": 1,
    "Tennis Balls": 1,
    "Monitor": 2,
    "Fire": 5,
    "Clouds": 5,
    "Wave": 5,
    "Spider Web": 2,
    "Stick": 2,
    "Leaf": 2,
    "Hearts": 2,
    "Book": 2,
    "Matrix": 3,
    "Rainbow": 3,
    "Brick Wall": 4,
    "Road": 3,
    "Beach": 5,
    "Sunset": 4,
    "City": 4,
    "Bedroom": 1,
}

backgrounds = {}
backgrounds.update(simple_backgrounds)
backgrounds.update(unique_backgrounds)

spots = {
    "Black Spots A": 0.5,
    "Black Spots B": 1,
    "Red Spots A": 0.5,
    "Red Spots B": 1,
    "Yellow Spots A": 0.5,
    "Yellow Spots B": 1,
}
colors = {
    "Red": 1,
    "Blue": 1,
    "Black": 1,
    "Green": 1,
    "Yellow": 1,
    "Orange": 1,
    "Purple": 1,
    "Camo": 1,
    "Gold": 0.01,
}

accessories = {
    None: 2,
    "Sombrero": 3,
    "Top Hat": 3,
    "Turban": 1,
    "Crown": 3,
    "Construction Hat": 2,
    "Graduation Cap": 2,
    "Beanie": 1,
    "Chef Cap": 3,
    "Bikini": 2,
    "Viking Helmet": 3,
    "Belt": 2,
    "Wizard Hat": 3,
    "Beach Hat": 3,
    "Halo": 3,
    "Clown Hat": 3,
    "Red Hair": 2,
    "Pirate Hat": 1.5,
    "Tux": 3,
    "Bathrobe": 2,
    "Cloak": 0.1,
    "Snorkel Gear": 1,
    "Red Sunglasses": 0.25,
    "Grey Sunglasses": 0.25,
}

eyes = {
    "Blue": 1,
    "Red": 1,
    "White": 1,
    "Grey": 0.25,
}

TOTAL_BUGS = (
        len(backgrounds)
        * len(spots)
        * len(colors)
        * len(accessories)
        * len(eyes)
)

currentlocation = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
outputlocation = os.path.join(currentlocation, './output/')

unique_backgrounds_with_accessories = {
    'Beach': ['Red Sunglasses', 'Grey Sunglasses', 'Bikini', 'Beach Hat', 'Pirate Hat'],
    'Book': ['Graduation Cap'],
    'Brick Wall': ['Construction Hat'],
    'City': ['Tux'],
    'Clouds': ['Red Sunglasses', 'Grey Sunglasses'],
    'Fire': ['Cloak'],
    'Spider Web': ['Wizard Hat'],
    'Sunset': ['Grey Sunglasses'],
    'Wave': ['Red Sunglasses', 'Grey Sunglasses', 'Bikini', 'Beach Hat', 'Pirate Hat'],
    'Bedroom': ['Bathrobe'],
}


def is_combo(trait):
    return (trait['Background'] in unique_backgrounds_with_accessories and
            trait['Accessory'] in unique_backgrounds_with_accessories[trait['Background']])


def get_combo_key(trait):
    return '{}:{}'.format(trait['Background'], trait['Accessory'])


def allowed_accessories_as_ignore_combination(background, allowed):
    aa = [a for a in allowed]
    aa.append(None)

    return {
        'Background': [background],
        'Accessory': set([a for a in list(accessories.keys()) if a not in aa])
    }


def get_ignored_combinations():
    accessories_without_none = list(accessories.keys())
    accessories_without_none.remove(None)

    ignore_combinations = [
        # Ignore Yellow spots with Yellow or Orange colored bugs
        {'Spots': ['Yellow Spots A', 'Yellow Spots B'],
         'Color': ['Yellow', 'Orange']},

        # Ignore Red spots with Red Colored Bugs
        {'Spots': ['Red Spots A', 'Red Spots B'], 'Color': ['Red', 'Purple']},

        # Ignore Green Colored bug with Matrix or Leaf Background
        {'Color': ['Green'], 'Background': ['Matrix', 'Leaf']},

        # Ignore bikini accessory with red spots
        {"Accessory": ['Bikini'], 'Spots': ['Red Spots A', 'Red Spots B']},

        # Ignore cloak with Red Pink background
        {"Accessory": ["Cloak"], 'Background': ['Red Pink']},

        # Ignore bikini accessory with red or purple colored bugs
        {"Accessory": ['Bikini'], 'Color': ['Red', 'Purple']},

        # Ignore Wizard hat accessory with blue black or red blue backgrounds
        {"Accessory": ["Wizard Hat"], "Background": ['Blue Black', 'Red Blue']},

        # Ignore pirate hat and cloak  accessory with Purple Blue background
        {"Accessory": ["Pirate Hat", "Cloak"], "Background": ['Purple Blue']},

        # Ignore snorkel gear with orange color bug
        {"Accessory": ["Snorkel Gear"], "Color": ["Orange"]},

        # Ignore red sunglasses with red bug
        {"Accessory": ["Red Sunglasses"], "Color": ["Red"]},

        # Ignore grey sunglasses with red bug
        {"Accessory": ["Grey Sunglasses"], "Color": ["Black"]},

        # Ignore graduation cap with black color bug
        {"Accessory": ["Graduation Cap"], "Color": ["Black"]},

        # Ignore gold color with gold background
        {"Color": ["Gold"], "Background": ["Gold"]},

        # Ignore gold color with unique backgrounds
        {"Color": ["Gold"], "Background": list(unique_backgrounds.keys())},

        {"Color": ["Gold"],
         "Accessory": ["Sombrero", "Construction Hat", "Beanie", "Chef Cap", "Bikini", "Belt", "Wizard Hat",
                       "Beach Hat", "Halo", "Clown Hat", "Pirate Hat", "Cloak", "Snorkel Gear", "Red Sunglasses",
                       "Grey Sunglasses"]},

        {"Background": ["Gold"], "Eyes": ["Grey", "White"]},

        {"Background": ["Gold"],
         "Accessory": ["Sombrero", "Construction Hat", "Beanie", "Chef Cap", "Bikini", "Belt", "Wizard Hat",
                       "Beach Hat", "Halo", "Clown Hat", "Pirate Hat", "Cloak", "Snorkel Gear", "Red Sunglasses",
                       "Grey Sunglasses"]},

        {"Color": ["Gold"], 'Spots': ['Yellow Spots A', 'Yellow Spots B', 'Red Spots A', 'Red Spots B']}
    ]

    for bg in unique_backgrounds:
        if bg in unique_backgrounds_with_accessories:
            ignore_combinations.append(
                allowed_accessories_as_ignore_combination(bg, unique_backgrounds_with_accessories[bg]))
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

    return False


def createCombo():
    trait = {
        "Background": random.choices(list(backgrounds.keys()), list(backgrounds.values()))[0],
        "Spots": random.choices(list(spots.keys()), list(spots.values()))[0],
        "Color": random.choices(list(colors.keys()), list(colors.values()))[0],
        "Accessory": random.choices(list(accessories.keys()), list(accessories.values()))[0],
        "Eyes": random.choices(list(eyes.keys()), list(eyes.values()))[0],
    }

    if trait['Accessory'] == 'Tux':
        trait['Color'] = None
        trait['Spots'] = None

    elif trait['Accessory'] == 'Bathrobe':
        trait['Spots'] = None

    elif trait["Accessory"] in ("Red Sunglasses", "Grey Sunglasses", "Snorkel Gear"):
        trait["Eyes"] = None

    return trait


def get_trait_key(trait):
    trait_key = (
        f"Accessory:{trait['Accessory']}"
        f",Background:{trait['Background']}"
        f",Color:{trait['Color']}"
        f",Eyes:{trait['Eyes']}"
        f",Spots:{trait['Spots']}"
    )

    return trait_key


def allUnique(x):
    seen = list()
    return not any(i in seen or seen.append(i) for i in x)


def generateCombinations(n, excluded_traits=None):
    if excluded_traits is None:
        excluded_traits = []

    traits = []
    trait_keys = set()
    excluded_trait_keys = set([get_trait_key(trait) for trait in excluded_traits])

    for i in tqdm(
            iterable=range(n),
            desc="Generating {} combinations".format(n),
            total=n,
            unit="combos",
    ):
        trait = createCombo()
        trait_key = get_trait_key(trait)

        while trait_key in trait_keys or shouldIgnore(trait) or trait_key in excluded_trait_keys:
            trait = createCombo()
            trait_key = get_trait_key(trait)

        trait_keys.add(trait_key)
        traits.append(trait)

    return traits


def getImage(img):
    if "None" not in img:
        return Image.open(img).convert('RGBA')

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
        im1 = getImage(os.path.join(currentlocation, 'Backgrounds', f'{trait["Background"]}.png'))
        im2 = getImage(os.path.join(currentlocation, 'Bugs', 'Small.png'))
        im3 = getImage(os.path.join(currentlocation, 'Colors', f'{trait["Color"]}.png'))
        im4 = getImage(os.path.join(currentlocation, 'Spots', f'{trait["Spots"]}.png'))
        im5 = getImage(os.path.join(currentlocation, 'Eyes', f'{trait["Eyes"]}.png'))
        im6 = getImage(os.path.join(currentlocation, 'Accessories', f'{trait["Accessory"]}.png'))

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
        if is_combo(trait):
            combo_to_severity = {
                'Wave:Beach Hat': 'Minor',
                'Beach:Beach Hat': 'Minor',
                'City:Tux': 'Blocker',
                'Beach:Pirate Hat': 'Trivial',
                'Wave:Grey Sunglasses': 'Trivial',
                'Brick Wall:Construction Hat': 'Trivial',
                'Wave:Pirate Hat': 'Trivial',
                'Beach:Red Sunglasses': 'Blocker',
                'Spider Web:Wizard Hat': 'Minor',
                'Fire:Cloak': 'Blocker',
                'Book:Graduation Cap': 'Major',
                'Beach:Bikini': 'Critical',
                'Wave:Bikini': 'Major',
                'Clouds:Red Sunglasses': 'Minor',
                'Sunset:Grey Sunglasses': 'Critical',
                'Beach:Grey Sunglasses': 'Minor',
                'Clouds:Grey Sunglasses': 'Minor',
                'Wave:Red Sunglasses': 'Minor',
            }
            combo_key = get_combo_key(trait)
            trait['Severity'] = combo_to_severity[combo_key]

        elif trait['Background'] == 'Gold' or trait['Color'] == 'Gold':
            trait['Severity'] = 'Blocker'

        elif trait['Accessory'] in ('Tux', 'Cloak', 'Bikini') or trait['Background'] in ('Matrix', 'Fire', 'Rainbow1'):
            trait['Severity'] = 'Blocker'

        elif trait['Accessory'] in ('Red Hair', 'Beach Hat') or trait['Background'] in ('Sunset', 'City'):
            trait['Severity'] = 'Critical'

        elif trait['Accessory'] in ('Crown', 'Viking Helmet', 'Halo', 'Top Hat') or trait['Background'] in ('Stick',):
            trait['Severity'] = 'Major'

        elif (trait['Accessory'] in ('Bathrobe', 'Turban', 'Pirate Hat', 'Belt', 'Construction Hat', 'Chef Cap') or
              trait['Background'] in ('American Football', 'Tennis Ball', 'Leaf', 'Monitor', 'Hearts', 'Spider Web')):
            trait['Severity'] = 'Minor'

        else:
            trait['Severity'] = 'Trivial'

    for trait in traits:
        assert 'Severity' in trait
        assert trait['Severity'] in ['Blocker', 'Critical', 'Major', 'Minor', 'Trivial']

    return traits


def count_traits(traits):
    # GET TRAIT COUNTS

    background_counts = defaultdict(int)
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
    print_csv(spots_counts)
    print_csv(color_counts)
    print_csv(accessory_count)
    print_csv(eyes_count)
    print_csv(combo_count)
    print_csv(severity_count)


def print_csv(d):
    for key, value in d.items():
        print("{},{}".format(key, value))
