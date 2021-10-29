from PIL import Image

directory = "./output"


def getNearestSquare(n):
    i = 1
    while i * i < n:
        i += 1

    return i


def combine(total):
    print("combining {} files".format(total))

    ns = getNearestSquare(total)

    final = Image.new('RGBA', (ns * 24, ns * 24))

    imgNo = 0

    for i in range(ns):
        for j in range(ns):
            if imgNo >= total:
                continue

            file = '{}.png'.format(imgNo)
            im1 = Image.open(directory + '/' + file).convert('RGBA')

            final.paste(im1, (j * 24, i * 24))

            imgNo += 1

    final.save('combined.png')
