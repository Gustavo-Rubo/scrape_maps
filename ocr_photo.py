import json
import time
import random
import easyocr
import numpy as np
from os import path
from PIL import Image
import PIL.ExifTags
from glob import glob

easyocr_reader = easyocr.Reader(['pt', 'en'])
reprocess_existing = True

def dms_to_dec(dms):
    return float(dms[0])+float(dms[1])/60+float(dms[2])/3600

def get_lat_long(img):
    exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if k in PIL.ExifTags.TAGS
    }
    lat = (-1 if exif['GPSInfo'][1] == 'S' else 1) * dms_to_dec(exif['GPSInfo'][2])
    long = (-1 if exif['GPSInfo'][3] == 'W' else 1) * dms_to_dec(exif['GPSInfo'][4])

    return lat, long

def ocr(file_og):
    file = path.split(file_og)[1]
    panoid = file.split('=')[0]
    # source = 'google' if len(panoid) <= 23 else 'user'

    img = Image.open(file_og)
    canvas_size = 2100
    exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if img._getexif() != None
        and k in PIL.ExifTags.TAGS
    }
    lat = (-1 if exif['GPSInfo'][1] == 'S' else 1) * dms_to_dec(exif['GPSInfo'][2])
    long = (-1 if exif['GPSInfo'][3] == 'W' else 1) * dms_to_dec(exif['GPSInfo'][4])

    easyocr_res = easyocr_reader.readtext(np.array(img),
        batch_size=1, detail=0, text_threshold=.6, canvas_size=canvas_size)
    easyocr_res.extend(easyocr_reader.readtext(np.array(img.rotate(-90, expand=1)),
        batch_size=1, detail=0, text_threshold=.6, canvas_size=canvas_size))
    

    return {
        'panoid': '',
        'lat': lat,
        'long': long,
        'source': 'photo',
        'file': file,
        'ocr': easyocr_res
    }


paths = glob(path.join('photos', '*'))
paths = [path for path in paths if path[-4] == '.']

old_data = []
if not reprocess_existing:
    with open(path.join('data', 'database_photos.json'), 'r') as f:
        old_data = json.load(f)
    new_paths = []
    old_panoids = [d['panoid'] for d in old_data]
    for p in paths:
        panoid = path.split(p)[1].split('=')[0]
        if panoid not in old_panoids:
            new_paths.append(p)

    paths = new_paths

random.shuffle(paths)

start = time.time()
data = []
# batch = 800
# for i, p in enumerate(paths[:batch]):
#     print(f'ocr {i+1}/{len(paths[:batch])}')
#     data.append(ocr(p))
for i, p in enumerate(paths):
    print(f'ocr {i+1}/{len(paths)}')
    data.append(ocr(p))
stop = time.time()

new_data = [*old_data, *data]

print(f'performed ocr in {len(data)} files')
print(f'run time: {stop - start:.0f}s')
print(f'time per file: {(stop - start)/len(paths):.2f}s')

with open(path.join('data', 'database_photos.json'), 'w') as f:
    json.dump(new_data, f)
