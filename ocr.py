import pytesseract
import numpy as np
from glob import glob
from os import path
from multiprocessing import Pool
import json
import time

reprocess_existing = False


def ocr(file_og):
    file = path.split(file_og)[1]
    panoid = file[:-44]
    source = 'google' if len(panoid) <= 23 else 'user'
    long = float(file[:-5].split('_')[-2])
    lat = float(file[:-5].split('_')[-1])

    res = pytesseract.image_to_string(
        file_og, nice=-10, lang='por+eng').split('\n')
    res = np.array(res)
    res = res[[len(r) >= 5 for r in res]]

    return {
        'panoid': panoid,
        'lat': lat,
        'long': long,
        'source': source,
        'thumb_file': file,
        'ocr': list(res)
    }


paths = glob(path.join('stitched', 'z5', '*'))
paths.extend(glob(path.join('stitched', 'z4', '*')))

start = time.time()
with Pool(12) as p:
    data = p.map(ocr, paths)
stop = time.time()

print(f'performed ocr in {len(paths)} files')
print(f'run time: {stop - start:.0f}s')
print(f'time per file: {(stop - start)/len(paths):.2f}s')

with open('database.json', 'w') as f:
    json.dump(data, f)
