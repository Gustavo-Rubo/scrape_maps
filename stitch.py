from PIL import Image, ImageOps
from os import path
from glob import glob

restitch_existing = False

def merge_images_z5(imgs):
    l = imgs[0].size[0]
    w = l * 24
    h = l * 3
    im = Image.new("RGB", (w, h))

    for j in range(3):
        for i in range(2, 14):
            im.paste(imgs[i+j*32], ((i-2)*l, j*l))

    for j in range(3):
        for i in range(18, 30):
            im.paste(imgs[i+j*32], ((i-6)*l, j*l))

    return im


def merge_images_z1(imgs):
    l = imgs[0].size[0]
    im = Image.new("RGB", (l*2, l))

    im.paste(imgs[0], (0, 0))
    im.paste(imgs[1], (l, 0))
    
    return im


for folder in glob('raw/z5/*'):
    stitched_file_name = path.join('stitched', 'z5', f'{folder.split("/")[-1]}.jpeg')

    if restitch_existing or not path.exists(stitched_file_name):
        stitches = []
        for file in sorted(glob(path.join(folder, '*'))):
            img = Image.open(file)
            stitches.append(img)
        
        merge_images_z5(stitches).save(stitched_file_name, compress_level=7)


for folder in glob('raw/z1/*'):
    stitched_file_name = path.join('stitched', 'z1', f'{folder.split("/")[-1]}.jpeg')

    if restitch_existing or not path.exists(stitched_file_name):
        stitches = []
        for file in sorted(glob(path.join(folder, '*'))):
            img = Image.open(file)
            stitches.append(img)

        merge_images_z1(stitches).save(stitched_file_name, compress_level=7)


