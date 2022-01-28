import glob
import os

from PIL import Image
import random
from collections import defaultdict

from tqdm import tqdm

simple_backgrounds = {
    "Gold": 0.05,

    "Beige": 3,
    "Light Blue": 3,
    "Dark Blue": 3,
    "Cyan": 3,
    "Green": 3,
    "Dirty Green": 3,
    "Light Green": 3,
    "Light Grey": 3,
    "Dirty Purple": 3,
    "Light Purple": 3,
    "Red": 3,
    "Light Red": 3,
    "Orange": 3,
    "Pink": 3,
    "Yellow": 3,
}

unique_backgrounds = {
    "Throne": 3,
    "Matrix": 3,

    "Fire": 4,
    "Chessboard": 4,
    "Book": 4,
    "Road": 4,
    "Bedroom": 4,
    "Classroom": 4,
    "Storefront": 4,

    "January": 4,
    "February": 4,
    "March": 4,
    "April": 4,
    "May": 4,
    "June": 4,
    "July": 4,
    "August": 4,
    "September": 4,
    "October": 4,
    "November": 4,
    "December": 4,

    "Stick": 5,
    "Beach": 5,
    "Clouds": 5,
    "Wave": 5,
    "Leaf": 5,
    "Hearts": 5,
    "Monitor": 5,
    "Spider Web": 5,
    "American Football": 5,
    "Tennis Balls": 5,

    "Sunset": 6,
    "Sun": 6,
    "Night Sky": 6,
    "Bush": 6,
    "Stream": 6,
    "Waterfall": 6,
    "Snow": 6,
    "Island": 6,
    "Rainbow": 6,
    "Desert": 6,
    "Trees": 6,
    "Mountains": 6,
    "Brick Wall": 6,
    "City": 6,
    "Pillars": 6,

}

backgrounds = {}
backgrounds.update(simple_backgrounds)
backgrounds.update(unique_backgrounds)

spots = {
    # "Red": 1,
    # "Yellow": 1,
    # "Cyan": 1,
    # "Pink": 1,

    "Zero": 0.01,
    "Two Black": 0.2,
    "Twelve Black": 0.5,
    "Three Black Stripes": 0.05,
    "Seven Black": 1,
    "Thirteen Black": 1,
    "Fourteen Orange": 0.2,
    "Fifteen Black": 0.25,
    "Twenty Black": 0.25,

    "Twenty Brown": 0.5,
    "Twenty Two Black": 0.5,
    "Twenty Four Black": 0.5,
    "Twenty Eight Black": 0.25,
}
colors = {
    "Gold": 0.3,
    "Blue": 1,
    "Green": 1,
    "Camo": 1,

    "Black": 0.2,
    "Orange": 1,
    "Purple": 1,
    "Yellow": 1,
    "Pink": 1,
    "Red": 1,
    "White": 1,
    "Cream": 1,
}

accessories = {
    "Crown": 1,
    "Halo": 1,
    "Tux": 1,
    "Horns": 1,
    "Shield": 1,

    None: 3,

    "Red Sunglasses": 2,
    "Red Hair": 2,
    "Bathrobe": 2,
    "Graduation Cap": 2,
    "Snorkel Gear": 2,
    "Top Hat": 2,

    "Viking Helmet": 3,
    "Beach Hat": 3,
    "Astronaut Helmet": 3,
    "Motorcycle Helmet": 3,

    "Chef Cap": 4,
    "Wizard Hat": 4,
    "Sombrero": 4,

    "Beanie": 5,
    "Pirate Hat": 5,
    "Construction Hat": 5,
    "Clown Hat": 5,
    "Big Green Glasses": 5,
    "Cowboy Hat": 5,
    "Ear Muffs": 5,
    "Life Vest": 5,
    "Santa Hat": 5,

    "Belt": 6,
    "Turban": 6,
    "Bikini": 6,

    "Bow": 7,
    "Pom Pom Hat": 7,
    "Sash": 7,
    "Umbrella": 7,
    "Baseball Cap": 7,
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
    'Beach': ['Red Sunglasses', 'Bikini', 'Beach Hat', 'Pirate Hat', "Life Vest", "Snorkel Gear"],
    'Book': ['Graduation Cap'],
    'Brick Wall': ['Construction Hat'],
    'City': ['Tux'],
    'Clouds': ['Red Sunglasses', "Life Vest"],
    'Spider Web': ['Wizard Hat'],
    'Wave': ['Red Sunglasses', 'Bikini', 'Beach Hat', "Life Vest", "Snorkel Gear"],
    'Bedroom': ['Bathrobe', "Ear Muffs"],
    "Desert": ["Sombrero", "Cowboy Hat"],
    "Snow": ["Beanie", "Ear Muffs", "Santa Hat"],
    "Island": ["Red Sunglasses", "Bikini", "Beach Hat", "Pirate Hat", "Life Vest", "Snorkel Gear"],
    "Night Sky": ["Beanie", "Tux", "Astronaut Helmet", "Bow", "Horns", "Santa Hat", "Halo"],
    "Mountains": ["Red Sunglasses"],
    "American Football": ["Baseball Cap"],
    "Tennis": ["Baseball Cap"],
    "Bush": ["Red Sunglasses", "Wizard Hat"],
    "Storefront": ["Red Sunglasses", "Red Hair", "Motorcycle Helmet"],
    "Stream": ["Life Vest", "Red Sunglasses", "Bikini", "Beach Hat", "Snorkel Gear"],
    "Waterfall": ["Life Vest", "Red Sunglasses", "Bikini", "Beach Hat"],
    "Throne": ["Crown", "Sash", "Tux"],
    "Pillars": ["Shield"],
    "Road": ["Motorcycle Helmet"],
    "Classroom": ["Graduation Cap"],
    # 'Sunset': ['Tux'],  # In two minds about this
    "Sun": ["Tux"],
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
        {'Spots': ['Yellow'], 'Background': ['Matrix', 'Tennis Balls', "Throne"]},

        {'Spots': ['Cyan'], 'Color': ['Yellow', 'Gold', 'Green', 'Orange', "Red"]},

        {'Spots': ['Cyan'], 'Eyes': ['Blue']},

        {'Spots': ['Cyan'], 'Background': ['Beach', 'Snow', 'Light Green', 'Cyan']},

        {'Spots': ['Pink'], 'Eyes': ['Red']},

        {'Spots': ['Pink'], 'Color': ['Orange', 'Gold', 'Purple', 'Red', "Yellow", "Green"]},

        {'Spots': ['Pink'], 'Background': ['Pink', "Throne"]},

        {'Spots': ['Pink'], 'Accessory': ['Snorkel Gear']},

        {'Eyes': ['Green'], 'Color': ['Green']},

        {'Accessory': ['Viking Helmet', 'Beach Hat'], 'Background': ['Beige']},

        # Ignore Red spots with Red Colored Bugs
        {'Spots': ['Red', ], 'Color': ['Red', 'Purple', 'Gold', "Camo", "Orange", "Black"]},

        # Ignore Green Colored bug with Matrix or Leaf Background
        {'Color': ['Green'], 'Background': ['Matrix', 'Leaf']},

        # Ignore bikini accessory with red spots
        {"Accessory": ['Bikini'], 'Spots': ['Red', ]},

        # Ignore red eyes with red spots
        {"Eyes": ["Red"], 'Spots': ['Red', ]},

        # Ignore bikini accessory with red or purple colored bugs
        {"Accessory": ['Bikini'], 'Color': ['Red', 'Purple']},

        # Ignore Wizard hat accessory with blue black or red blue backgrounds
        {"Accessory": ["Wizard Hat"], "Background": ['Blue Black', 'Red Blue']},

        # Ignore pirate hat accessory with Purple Blue background
        {"Accessory": ["Pirate Hat"], "Background": ['Purple Blue', 'Blue Black']},

        {"Accessory": ["Snorkel Gear", "Astronaut Helmet"], "Color": ["Orange"]},

        # Ignore red sunglasses with red bug
        {"Accessory": ["Red Sunglasses"], "Color": ["Red"]},

        # Ignore gold color with gold background
        {"Color": ["Gold"], "Background": ["Gold"]},

        # Ignore gold color with unique backgrounds
        {"Color": ["Gold"], "Background": list(unique_backgrounds.keys())},

        {"Color": ["Gold"],
         "Accessory": [
             "Sombrero", "Construction Hat", "Beanie", "Chef Cap", "Bikini", "Belt", "Wizard Hat",
             "Beach Hat", "Halo", "Clown Hat", "Pirate Hat", "Snorkel Gear", "Red Sunglasses",
             "Bow", "Big Green Glasses", "Astronaut Helmet", "Baseball Cap", "Umbrella", "Horns",
             "Cowboy Hat", "Ear Muffs", "Motorcycle Helmet",
         ]},

        {"Background": ["Gold"], "Eyes": ["Grey", "White"]},

        {"Background": ["Gold"],
         "Accessory": [
             "Sombrero", "Construction Hat", "Beanie", "Chef Cap", "Bikini", "Belt", "Wizard Hat",
             "Beach Hat", "Clown Hat", "Pirate Hat", "Snorkel Gear", "Red Sunglasses",
             "Bow", "Astronaut Helmet", "Baseball Cap", "Umbrella", "Cowboy Hat", "Ear Muffs",
             "Motorcycle Helmet", "Life Vest"
         ]},

        {"Background": ["Yellow"],
         "Accessory": ["Construction Hat", "Beanie", "Beach Hat", "Viking Helmet", "Sombrero", "Graduation Cap",
                       "Ear Muffs"]},
        {"Background": ["Orange"], "Accessory": ["Construction Hat", "Sombrero", "Ear Muffs"]},
        {"Background": ["Monitor", "Red Blue", "Blue Black"], "Color": ["Black"]},
        {"Background": ["Monitor", "Red Blue", "Stick", "Blue Black"], "Color": ["Camo"]},
        {"Accessory": ["Pirate Hat", "Graduation Cap"], "Color": ["Black"]},
        {"Background": ["Book", "Bedroom"], "Color": ["Yellow"]},
        {"Background": ["Desert", "Orange"], "Color": ["Orange"]},

        {"Background": ["Trees", "Stream"], "Color": ["Green"]},

        {"Background": ["Blue Black"], "Color": ["Blue", "Black", "Camo", "Gold"]},
        {"Background": ["Spider Web", "Sunset"], "Color": ["Black"]},
        {"Background": ["Night Sky"], "Color": ["Blue"]},
        {"Background": ["Night Sky"], "Spots": ["Pink", "Cyan", "Yellow", "Red"]},
        {"Eyes": ["White"],
         "Background": ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                        "October", "November", "December"]},
        {"Accessory": ["Crown", "Red Sunglasses"], "Background": ["Red"]},

        {"Color": ["Purple"], "Background": ["Light Purple", "Throne"]},

        {"Accessory": ["Bow"], "Spots": ["Yellow", "Cyan"]},
        {"Accessory": ["Bow", "Ear Muffs"], "Color": ["Yellow"]},
        {"Accessory": ["Sash"], "Spots": ["Cyan", "Yellow"]},

        {"Accessory": ["Shield"], "Color": ["Purple"]},

        {"Accessory": ["Pom Pom Hat"], "Background": ["Light Red", "Pink"]},

        {"Accessory": ["Horns"], "Background": ["Red"]},

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


def create_combo():
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

    elif trait['Accessory'] == 'Bathrobe' or trait['Accessory'] == 'Shield':
        trait['Spots'] = None

    elif trait["Accessory"] in ("Red Sunglasses", "Snorkel Gear", "Motorcycle Helmet",
                                "Astronaut Helmet", "Big Green Glasses",):
        trait["Eyes"] = None

    if trait['Spots'] in ('Zero', 'Two Black', 'Three Black Stripes'):
        trait['Color'] = 'Red'

    elif trait['Spots'] == 'Twelve Black':
        trait['Color'] = 'Pink'

    elif trait['Spots'] == 'Fourteen Orange':
        trait['Color'] = 'Black'

    elif trait['Spots'] == 'Fifteen Black':
        cs = ['White', 'Purple']
        trait['Color'] = random.choices(cs, [w for c, w in colors.items() if c in cs])[0]

    elif trait['Spots'] == 'Twenty Brown':
        trait['Color'] = 'Cream'

    elif trait['Spots'] == 'Twenty Black':
        trait['Color'] = 'White'

    elif trait['Spots'] == 'Twenty Two Black':
        trait['Color'] = 'Yellow'

    elif trait['Spots'] == 'Twenty Four Black':
        trait['Color'] = 'Orange'

    elif trait['Spots'] == 'Twenty Eight Black':
        cs = ['Orange']
        trait['Color'] = random.choices(cs, [w for c, w in colors.items() if c in cs])[0]

    if trait['Color'] == 'Cream':
        trait['Spots'] = 'Twenty Brown'

    elif trait['Color'] == 'White' and trait['Spots'] not in ['Twenty Black', 'Fifteen Black']:
        ss = ['Twenty Black', 'Fifteen Black']
        trait['Spots'] = random.choices(ss, [w for s, w in spots.items() if s in ss])[0]

    elif trait['Color'] == 'Black':
        trait['Spots'] = 'Fourteen Orange'

    elif trait['Color'] == 'Yellow' and trait['Spots'] not in ['Twenty Two Black']:
        ss = ['Twenty Two Black']
        trait['Spots'] = random.choices(ss, [w for s, w in spots.items() if s in ss])[0]

    elif trait['Color'] == 'Orange' and trait['Spots'] not in ['Twenty Four Black', 'Twenty Eight Black']:
        ss = ['Twenty Four Black', 'Twenty Eight Black']
        trait['Spots'] = random.choices(ss, [w for s, w in spots.items() if s in ss])[0]

    elif trait['Color'] == 'Purple':
        trait['Spots'] = 'Fifteen Black'

    elif trait['Color'] == 'Pink':
        trait['Spots'] = 'Twelve Black'

    elif trait['Color'] == 'Red' and trait['Spots'] not in ['Zero', 'Two Black', 'Three Black Stripes',
                                                            'Seven Black', 'Thirteen Black']:
        ss = ['Zero', 'Two Black', 'Three Black Stripes', 'Seven Black', 'Thirteen Black']
        trait['Spots'] = random.choices(ss, [w for s, w in spots.items() if s in ss])[0]

    elif trait['Color'] in ['Gold', 'Blue', 'Green', 'Camo'] and trait['Spots'] not in ['Seven Black',
                                                                                        'Thirteen Black']:
        ss = ['Seven Black', 'Thirteen Black']
        trait['Spots'] = random.choices(ss, [w for s, w in spots.items() if s in ss])[0]

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
    trait_csa_keys = set()
    excluded_trait_keys = set([get_trait_key(trait) for trait in excluded_traits])

    for i in tqdm(
            iterable=range(n),
            desc="Generating {} combinations".format(n),
            total=n,
            unit="combos",
    ):
        trait = create_combo()
        trait_key = get_trait_key(trait)
        trait_csa_key = get_trait_csa_key(trait)

        while trait_key in excluded_trait_keys or shouldIgnore(trait) or trait_csa_key in trait_csa_keys:
            trait = create_combo()
            trait_key = get_trait_key(trait)
            trait_csa_key = get_trait_csa_key(trait)

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
    accessory_counts = defaultdict(int)
    eyes_counts = defaultdict(int)
    combo_counts = defaultdict(int)

    for trait in tqdm(
            iterable=traits,
            desc="Counting individual traits in {}".format(len(traits)),
            unit="trait",
            total=len(traits),
    ):

        spots_counts[trait["Spots"]] += 1
        color_counts[trait["Color"]] += 1
        eyes_counts[trait["Eyes"]] += 1
        background_counts[trait["Background"]] += 1
        accessory_counts[trait["Accessory"]] += 1

        if is_combo(trait):
            combo_counts[get_combo_key(trait)] += 1

    return background_counts, spots_counts, color_counts, accessory_counts, eyes_counts, combo_counts


def print_csv(label, d):
    total = sum(d.values())
    csv = {}

    print("----------------")
    print(label)
    print("----------------")

    for key, value in d.items():
        csv[key] = (value, round(value / total * 100, 2))

    for i in sorted(csv.items(), key=lambda x: x[1][0]):
        print("{},{},{}".format(i[0], i[1][0], i[1][1]))
