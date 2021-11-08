from PIL import Image

directory = './output'
file = '10.png'
im1 = Image.open(directory + '/' + file).convert('RGBA')

im1 = im1.resize((240, 240), Image.NEAREST)

im1.save(directory + '/' + file)
