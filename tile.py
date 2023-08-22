import requests
import shutil
import numpy as np
from os import path, makedirs

base_streetview_url = 'https://streetviewpixels-pa.googleapis.com/v1/tile?cb_client=maps_sv.tactile'
# panoids = ['eTPYmbok7Ho94LG2bW9XgA', 'tQbB6SQ_anc7hOUEJNxHfg', 'Bpw-92VrITn2LIim3gzlZw', 'wS2g9Ay4DqTuOPOQ5fPErg']
panoids = np.load('panoids.npy')

count = 0
for panoid in panoids:
    print(f'{count}/{len(panoids)}')
    count += 1
    z = 1
    makedirs(path.join('raw', f'z{z}', '_'.join(panoid)), exist_ok=True)

    # for y in range(int(2**max(0, z-1))):
    for y in [0]:
        for x in [0, 1]:
            url = base_streetview_url + f'&panoid={panoid[0]}&x={x}&y={y}&zoom={z}&nbt=1&fover=2'
            img = requests.get(url, stream=True)

            if img.status_code == 200:
                with open(path.join('raw', f'z{z}', '_'.join(panoid), f'z{z}-y{y:02}-x{x:02}.jpeg'), 'wb') as f:
                    shutil.copyfileobj(img.raw, f)

    z = 5
    makedirs(path.join('raw', f'z{z}', '_'.join(panoid)), exist_ok=True)

    # for y in range(int(2**max(0, z-1))):
    for y in range(7, 10):
        for x in range(int(2**z)):
            url = base_streetview_url + f'&panoid={panoid[0]}&x={x}&y={y}&zoom={z}&nbt=1&fover=2'
            img = requests.get(url, stream=True)

            if img.status_code == 200:
                with open(path.join('raw', f'z{z}', '_'.join(panoid), f'z{z}-y{y:02}-x{x:02}.jpeg'), 'wb') as f:
                    shutil.copyfileobj(img.raw, f)