import os

from PIL import Image, ImageOps

directory = "./output"
images = [file for file in os.listdir(directory) if file.endswith(".png")]
total = len(images)


def getNearestSquare(n):
    i = 1
    while i * i < n:
        i += 1

    return i


def combine():
    print("combining {} files".format(total))

    ns = getNearestSquare(total)

    final = Image.new('RGBA', (ns * 24, ns * 24))

    print(images)

    imgNo = 0

    for i in range(ns):
        for j in range(ns):
            if len(images) == 0 or imgNo >= total:
                continue

            file = '{}.png'.format(imgNo)
            im1 = Image.open(directory + '/' + file).convert('RGBA')

            final.paste(im1, (j * 24, i * 24))

            imgNo += 1

    final.save('combined.png')
