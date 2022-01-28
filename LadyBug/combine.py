from collections import defaultdict

from PIL import Image
from tqdm import tqdm

directory = "./output"

SIZE = 120


def get_nearest_square(n):
    i = 1
    while i * i < n:
        i += 1

    return i


def combine_by_background(traits):
    traits_by_background = defaultdict(list)
    for trait in traits:
        traits_by_background[trait['Background']].append(trait)

    for background, traits in traits_by_background.items():
        combine(traits, combined_file_name='combined {}.png'.format(background))


def combine(traits, combined_file_name='combined.png'):
    # Sort for evaluation
    traits = sorted(traits,
                    key=lambda t: (
                        t['Background'] or 'None',
                        t['Color'] or 'None',
                        t['Spots'] or 'None',
                        t['Accessory'] or 'None',
                        t['Eyes'] or 'None',
                    ))

    total = len(traits)

    ns = get_nearest_square(total)

    final = Image.new('RGBA', (ns * 120, ns * 120))

    imgNo = 0

    with tqdm(total=total, desc="combining {} files".format(total), unit="image") as pbar:
        for i in range(ns):
            for j in range(ns):
                if imgNo >= total:
                    continue

                file = '{}.png'.format(traits[imgNo]['tokenId'])
                im1 = Image.open(directory + '/' + file).convert('RGBA')

                final.paste(im1, (j * 120, i * 120))

                imgNo += 1
                pbar.update(1)

    final.save(combined_file_name)


def combineToGif(traits):
    # Sort for evaluation
    traits = sorted(traits,
                    key=lambda t: (
                        t['Background'] or 'None',
                        t['Color'] or 'None',
                        t['Spots'] or 'None',
                        t['Accessory'] or 'None',
                        t['Eyes'] or 'None',
                    ))

    total = len(traits)

    images = []

    with tqdm(total=total, desc="reading {} images".format(total), unit="image") as pbar:
        for i in range(total):
            file = '{}.png'.format(traits[i]['tokenId'])
            im1 = Image.open(directory + '/' + file).convert('RGBA')
            im1 = im1.resize((SIZE, SIZE), Image.NEAREST)
            images.append(im1)
            pbar.update(1)

    images[0].save('combined.gif', save_all=True, append_images=images[1:],
                   optimize=False, duration=400, loop=0)
