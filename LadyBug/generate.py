import glob
import os

from PIL import Image
import random
from collections import defaultdict

from tqdm import tqdm

simple_backgrounds = {
    

    # "Purple Blue": 3,
    # "Red Blue": 3,
    # "Yellow Green": 3,
    # "Red Pink": 3,
    # "Blue Black": 3,
    # "Yellow Purple": 3,
    # "Light Red Light Blue": 3,
    
    "Beige":4,
    
    "Light Blue": 4,
    "Dark Blue": 4,
    
    "Cyan": 4,
    
    "Green": 4,
    "Dirty Green": 4,
    "Light Green": 4,
    
    "Gold": 0.1,
    
    "Light Grey": 4,
    
    "Dirty Purple": 4,
    "Light Purple": 4,
    
    "Red": 4,
    "Light Red": 4,
    
    "Orange": 4,
    
    "Pink": 4,
    
    "Yellow": 4,
}
unique_backgrounds = {
    "June": 2,

    "Bedroom": 2,
    "American Football": 2,
    "Tennis Balls": 2,

    "Monitor": 2,
    "Spider Web": 2,
    "Stick": 2,
    "Leaf": 2,
    "Hearts": 2,
    "Book": 2,
    "Snow": 2,
    "Matrix": 2,

    "Pillars": 3,
    "Island": 3,
    "Rainbow": 3,
    "Road": 3,
    "Desert": 3,
    "Trees": 3,

    "Brick Wall": 4,
    "Sunset": 4,
    "City": 4,

    "Beach": 5,
    "Fire": 5,
    "Clouds": 5,
    "Wave": 5,
    "Mountains": 2,
}

backgrounds = {}
backgrounds.update(simple_backgrounds)
backgrounds.update(unique_backgrounds)

spots = {
    "Black": 1,
    "Red": 1,
    "Yellow": 1,
    "Cyan": 1,
    "Pink": 1,
}
colors = {
    "Gold": 0.3,
    "Black": 0.5,

    "Red": 1,
    "Blue": 1,
    "Green": 1,
    "Yellow": 1,
    "Orange": 1,
    "Purple": 1,
    "Camo": 1,
}

accessories = {
    "Red Sunglasses": 0.25,

    "Turban": 1,
    "Beanie": 1,
    "Snorkel Gear": 1,

    "Pirate Hat": 1.5,

    None: 2,
    "Red Hair": 2,
    "Bathrobe": 2,
    "Belt": 2,
    "Construction Hat": 2,
    "Graduation Cap": 2,
    "Bikini": 2,

    "Viking Helmet": 3,
    "Chef Cap": 3,
    "Wizard Hat": 3,
    "Sombrero": 3,
    "Top Hat": 3,
    "Crown": 3,
    "Beach Hat": 3,
    "Halo": 3,
    "Clown Hat": 3,
    "Tux": 3,
}

eyes = {
    "Blue": 1,
    "Red": 1,
    "White": 1,
    "Green": 1,
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
    'Beach': ['Red Sunglasses', 'Bikini', 'Beach Hat', 'Pirate Hat'],
    'Book': ['Graduation Cap'],
    'Brick Wall': ['Construction Hat'],
    'City': ['Tux'],
    'Clouds': ['Red Sunglasses'],
    'Spider Web': ['Wizard Hat'],
    'Wave': ['Red Sunglasses', 'Bikini', 'Beach Hat'],
    'Bedroom': ['Bathrobe'],
    "Desert": ["Sombrero"],
    "Snow": ["Beanie"],
    "Island": ["Red Sunglasses", "Bikini", "Beach Hat", "Pirate Hat"],
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
        {'Spots': ['Yellow'], 'Color': ['Yellow', 'Orange', 'Red', 'Gold']},

        # Ignore Yellow spots with white eyes
        {'Spots': ['Yellow'], 'Eyes': ['White']},

        # Ignore Yellow spots with matrix
        {'Spots': [ 'Yellow'], 'Background': ['Matrix', 'Tennis Balls']},

        {'Spots': ['Cyan'], 'Color': ['Yellow', 'Gold', 'Green', 'Orange']},

        {'Spots': ['Cyan'], 'Eyes': ['Blue']},

        {'Spots': ['Cyan'], 'Background': ['Beach', 'Snow']},

        {'Spots': ['Pink'], 'Eyes': ['Red']},

        {'Spots': ['Pink'], 'Color': ['Orange', 'Gold', 'Purple', 'Red', ]},
        
        {'Spots': ['Pink'], 'Background': ['Pink'] },

        {'Spots': ['Pink'], 'Accessory': ['Snorkel']},
        
        {'Eyes': ['Green'], 'Color': ['Green']},

        {'Accessory': ['Viking Helmet', 'Beach Hat'], 'Background':['Beige']},

        # Ignore Red spots with Red Colored Bugs
        {'Spots': ['Red', ], 'Color': ['Red', 'Purple', 'Gold', "Camo", "Orange", "Black"]},

        # Ignore Green Colored bug with Matrix or Leaf Background
        {'Color': ['Green'], 'Background': ['Matrix', 'Leaf']},

        # Ignore bikini accessory with red spots
        {"Accessory": ['Bikini'], 'Spots': ['Red',]},

        # Ignore red eyes with red spots
        {"Eyes": ["Red"], 'Spots': ['Red', ]},

        # Ignore bikini accessory with red or purple colored bugs
        {"Accessory": ['Bikini'], 'Color': ['Red', 'Purple']},

        # Ignore Wizard hat accessory with blue black or red blue backgrounds
        {"Accessory": ["Wizard Hat"], "Background": ['Blue Black', 'Red Blue']},

        # Ignore pirate hat accessory with Purple Blue background
        {"Accessory": ["Pirate Hat"], "Background": ['Purple Blue', 'Blue Black']},

        # Ignore snorkel gear with orange color bug
        {"Accessory": ["Snorkel Gear"], "Color": ["Orange"]},

        # Ignore red sunglasses with red bug
        {"Accessory": ["Red Sunglasses"], "Color": ["Red"]},

        # Ignore gold color with gold background
        {"Color": ["Gold"], "Background": ["Gold"]},

        # Ignore gold color with unique backgrounds
        {"Color": ["Gold"], "Background": list(unique_backgrounds.keys())},

        {"Color": ["Gold"],
         "Accessory": ["Sombrero", "Construction Hat", "Beanie", "Chef Cap", "Bikini", "Belt", "Wizard Hat",
                       "Beach Hat", "Halo", "Clown Hat", "Pirate Hat", "Snorkel Gear", "Red Sunglasses"]},

        {"Background": ["Gold"], "Eyes": ["Grey", "White"]},

        {"Background": ["Gold"],
         "Accessory": ["Sombrero", "Construction Hat", "Beanie", "Chef Cap", "Bikini", "Belt", "Wizard Hat",
                       "Beach Hat", "Halo", "Clown Hat", "Pirate Hat", "Snorkel Gear", "Red Sunglasses"]},

        {"Background": ["Yellow"],
         "Accessory": ["Construction Hat", "Beanie", "Beach Hat", "Viking Helmet", "Sombrero", "Graduation Cap"]},
        {"Background": ["Orange"], "Accessory": ["Construction Hat"]},
        {"Background": ["Monitor", "Red Blue", "Stick", "Blue Black"], "Color": ["Black"]},
        {"Background": ["Monitor", "Red Blue", "Stick", "Blue Black"], "Color": ["Camo"]},
        {"Accessory": ["Pirate Hat", "Graduation Cap"], "Color": ["Black"]},
        {"Background": ["Book", "Bedroom"], "Color": ["Yellow"]},
        {"Background": ["Desert"], "Color": ["Orange"]},
        {"Background": ["Trees"], "Color": ["Green"]},
        {"Background": ["Blue Black"], "Color": ["Blue", "Black", "Camo", "Gold"]},
        {"Background": ["Spider Web", "Sunset"], "Color": ["Black"]},
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

    elif trait["Accessory"] in ("Red Sunglasses", "Snorkel Gear"):
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


def get_trait_csa_key(trait):
    trait_key = (
        f"Accessory:{trait['Accessory']}"
        f",Background:{trait['Background']}"
        f",Color:{trait['Color']}"
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
    trait_csa_keys = set()
    excluded_trait_keys = set([get_trait_key(trait) for trait in excluded_traits])

    for i in tqdm(
            iterable=range(n),
            desc="Generating {} combinations".format(n),
            total=n,
            unit="combos",
    ):
        trait = createCombo()
        trait_key = get_trait_key(trait)
        trait_csa_key = get_trait_csa_key(trait)

        while trait_key in trait_keys or trait_key in excluded_trait_keys or shouldIgnore(trait) or trait_csa_key in trait_csa_keys:
            trait = createCombo()
            trait_key = get_trait_key(trait)
            trait_csa_key = get_trait_csa_key(trait)


        trait_keys.add(trait_key)
        trait_csa_keys.add(trait_csa_key)
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


def count_traits(traits):
    # GET TRAIT COUNTS

    background_counts = defaultdict(int)
    spots_counts = defaultdict(int)
    color_counts = defaultdict(int)
    accessory_count = defaultdict(int)
    eyes_count = defaultdict(int)
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


def print_csv(d):
    total = sum(d.values())
    csv = {}

    for key, value in d.items():
        csv[key] = (value, round(value / total * 100, 2))

    for i in sorted(csv.items(), key=lambda x: x[1][0]):
        print("{},{},{}".format(i[0], i[1][0], i[1][1]))
