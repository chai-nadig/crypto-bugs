from PIL import Image, ImageOps
from IPython.display import display
import random
import json

backgrounds = [
    "SpiderWeb",
    "Stick",
    "Leaf",
    "Hearts",
    "Book",
    "Matrix",
    "Rainbow1",
    "Rainbow2",
    "Rainbow3",
]
backgroundweights = [1, 1, 1, 1, 1, 1, 1, 1, 1]

backgroundfiles = {
    "SpiderWeb": "SpiderWeb.png",
    "Stick": "Stick.png",
    "Leaf": "Leaf.png",
    "Hearts": "Hearts.png",
    "Book": "Book.png",
    "Matrix": "Matrix.png",
    "Rainbow1": "Rainbow1.png",
    "Rainbow2": "Rainbow2.png",
    "Rainbow3": "Rainbow3.png",
}

bugs = ["Small"]
bugweights = [1]

bugfiles = {
    "Small": "Small.png",
}

bigBugSpots = ["BigSpotsA", "BigSpotsB"]
bigBugSpotWeights = [1, 1]

smallBugSpots = [
    "SmallBlackSpotsA",
    "SmallBlackSpotsB",
    "SmallBlackSpotsC",
    "SmallDarkRedSpotsA",
    "SmallDarkRedSpotsB",
    "SmallDarkRedSpotsC",
    "SmallYellowSpotsA",
    "SmallYellowSpotsB",
    "SmallYellowSpotsC",
]
smallBugSpotsWeights = [
    1, 1, 1,
    1, 1, 1,
    1, 1, 1,
]

spotsfiles = {
    "BigSpotsA": "BigSpotsA.png",
    "BigSpotsB": "BigSpotsB.png",
    "SmallBlackSpotsA": "SmallBlackSpotsA.png",
    "SmallBlackSpotsB": "SmallBlackSpotsB.png",
    "SmallBlackSpotsC": "SmallBlackSpotsC.png",
    "SmallDarkRedSpotsA": "SmallDarkRedSpotsA.png",
    "SmallDarkRedSpotsB": "SmallDarkRedSpotsB.png",
    "SmallDarkRedSpotsC": "SmallDarkRedSpotsC.png",
    "SmallYellowSpotsA": "SmallYellowSpotsA.png",
    "SmallYellowSpotsB": "SmallYellowSpotsB.png",
    "SmallYellowSpotsC": "SmallYellowSpotsC.png",
}

bigColors = ["BigRed", "BigBlue"]
bigColorWeights = [1, 1]

smallColors = [
    "SmallRed",
    "SmallBlue",
    "SmallBlack",
    "SmallGreen",
    "SmallINFlag",
    "SmallYellow",
]
smallColorWeights = [
    1,
    1,
    1,
    1,
    1,
    1,
]

colorfiles = {
    "BigRed": "BigRed.png",
    "BigBlue": "BigBlue.png",
    "SmallRed": "SmallRed.png",
    "SmallBlue": "SmallBlue.png",
    "SmallBlack": "SmallBlack.png",
    "SmallGreen": "SmallGreen.png",
    "SmallINFlag": "SmallINFlag.png",
    "SmallYellow": "SmallYellow.png",
}

## TRAIT GENERATION
TOTAL_BUGS = 40

traits = []


def createCombo():
    trait = {}

    trait["Background"] = random.choices(backgrounds, backgroundweights)[0]
    trait["Bug"] = random.choices(bugs, bugweights)[0]

    if trait["Bug"] == "Big":
        trait["Spots"] = random.choices(bigBugSpots, bigBugSpotWeights)[0]
        trait["Color"] = random.choices(bigColors, bigColorWeights)[0]
    else:
        trait["Spots"] = random.choices(smallBugSpots, smallBugSpotsWeights)[0]
        trait["Color"] = random.choices(smallColors, smallColorWeights)[0]

    if trait in traits:
        return createCombo()
    else:
        return trait


for i in range(TOTAL_BUGS):
    newtraitcombo = createCombo()
    traits.append(newtraitcombo)


def allUnique(x):
    seen = list()
    return not any(i in seen or seen.append(i) for i in x)


print(allUnique(traits))

# ADD TOKEN IDS TO JSON

i = 0
for item in traits:
    item["tokenId"] = i
    i = i + 1

print(traits)

# GET TRAIT COUNTS
from collections import defaultdict

backgroundcounts = defaultdict(int)
bugcounts = defaultdict(int)
spotscounts = defaultdict(int)
colorcounts = defaultdict(int)

for bug in traits:
    backgroundcounts[bug["Background"]] += 1
    bugcounts[bug["Bug"]] += 1
    spotscounts[bug["Spots"]] += 1
    colorcounts[bug["Color"]] += 1

print("background:", backgroundcounts)
print("bugs:", bugcounts)
print("spots:", spotscounts)
print("colors:", colorcounts)

# WRITE METADATA TO JSON FILE

with open('traits2.json', 'w') as outfile:
    json.dump(traits, outfile, indent=4)

print(backgroundfiles)

# IMAGE GENERATION
for item in traits:
    im1 = Image.open(f'./Backgrounds/{backgroundfiles[item["Background"]]}').convert('RGBA')
    im2 = Image.open(f'./Bugs/{bugfiles[item["Bug"]]}').convert('RGBA')
    im3 = Image.open(f'./Colors/{colorfiles[item["Color"]]}').convert('RGBA')
    im4 = Image.open(f'./Spots/{spotsfiles[item["Spots"]]}').convert('RGBA')

    # final = Image.new('RGBA', im1.size)

    # Create each composite

    # final.paste(im1)
    # final.paste(im2)
    # final.paste(im3)
    # final.paste(im4)
    com1 = Image.alpha_composite(im1, im2)
    com2 = Image.alpha_composite(com1, im3)
    com3 = Image.alpha_composite(com2, im4)

    # Convert to RGB
    rgb_im = com3.convert('RGBA')
    #     display(rgb_im.resize((400,400), Image.NEAREST))

    file_name = str(item["tokenId"]) + ".png"
    rgb_im.save("./output/" + file_name)
    # final.save("./output/" + file_name)
    print(f'{str(item["tokenId"])} done')

print(traits)

with open('traitsfinal.json', 'w') as outfile:
    json.dump(traits, outfile, indent=4)
