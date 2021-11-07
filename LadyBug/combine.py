from PIL import Image
from tqdm import tqdm

directory = "./output"


def getNearestSquare(n):
    i = 1
    while i * i < n:
        i += 1

    return i


def combine(traits):
    # Sort for evaluation
    traits = sorted(traits,
                    key=lambda t: (t['Background'], t['Color'], t['Spots'], t['Accessory'], t['Eyes']))

    total = len(traits)

    ns = getNearestSquare(total)

    final = Image.new('RGBA', (ns * 24, ns * 24))

    imgNo = 0

    with tqdm(total=total, desc="combining {} files".format(total), unit="image") as pbar:
        for i in range(ns):
            for j in range(ns):
                if imgNo >= total:
                    continue

                file = '{}.png'.format(imgNo)
                im1 = Image.open(directory + '/' + file).convert('RGBA')

                final.paste(im1, (j * 24, i * 24))

                imgNo += 1
                pbar.update(1)

    final.save('combined.png')
