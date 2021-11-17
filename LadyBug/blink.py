from PIL import Image

directory = './blink'

images = []

imageOpen = Image.open(directory + '/0.png').convert('RGBA')
png_info = imageOpen.info

imageClosed = Image.open(directory + '/1.png').convert('RGBA')

frameCounts = [25, 5, 5, 5, 25]

SIZE = 120

open = True
for c in frameCounts:
    if open:
        images.extend([imageOpen.resize((SIZE, SIZE), Image.NEAREST).convert('RGBA') for i in range(c)])
    else:
        images.extend([imageClosed.resize((SIZE, SIZE), Image.NEAREST).convert('RGBA') for i in range(c)])

    open = not open

images[0].save('blink.gif', save_all=True, append_images=images[1:],
               optimize=True, duration=50, loop=1)
