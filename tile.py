import requests
import shutil
import numpy as np
from os import path, makedirs
from multiprocessing import Pool

redownload_existing = False


# panoids = ['eTPYmbok7Ho94LG2bW9XgA', 'tQbB6SQ_anc7hOUEJNxHfg', 'Bpw-92VrITn2LIim3gzlZw', 'wS2g9Ay4DqTuOPOQ5fPErg']
panoids = np.load('panoids.npy')
user_panoids = np.load('user_panoids.npy')

def download_and_save_tile(args): #x, y, z, panoid):    
    x = args[0]
    y = args[1]
    z = args[2]
    panoid = args[3]
    base_streetview_url = 'https://streetviewpixels-pa.googleapis.com/v1/tile?cb_client=maps_sv.tactile'
    url = base_streetview_url + f'&panoid={panoid[0]}&x={x}&y={y}&zoom={z}&nbt=1&fover=2'
    img = requests.get(url, stream=True)

    if img.status_code == 200:
        with open(path.join(base_dir, f'z{z}-y{y:02}-x{x:02}.jpeg'), 'wb') as f:
            shutil.copyfileobj(img.raw, f)
    else:
        print(img.status_code, x, y, z, panoid)

def download_and_save_user_tile(args): #x, y, z, user_panoid):
    x = args[0]
    y = args[1]
    z = args[2]
    user_panoid = args[3]
    base_streetview_url = 'https://lh3.ggpht.com/p/'
    url = base_streetview_url + f'{user_panoid[0]}=x{x}-y{y}-z{z}'
    img = requests.get(url, stream=True)

    if img.status_code == 200:
        with open(path.join(base_dir, f'z{z}-y{y:02}-x{x:02}.jpeg'), 'wb') as f:
            shutil.copyfileobj(img.raw, f)
    else:
        print(img.status_code, x, y, z, user_panoid)


for i, panoid in enumerate(panoids):
    print(f'{i+1}/{len(panoids)}')
    
    z = 1
    base_dir = path.join('raw', f'z{z}', '_'.join(panoid))
    if redownload_existing or not path.isdir(base_dir):
        makedirs(base_dir, exist_ok=True)

        # for y in range(int(2**max(0, z-1))):
        for y in [0]:
            with Pool(2) as p:
                args = [(c[0], *c[1]) for c in zip([b for b in range(2)], [[y, z, panoid]]*2)]

                p.map(download_and_save_tile, args)
            # for x in [0, 1]:
            #     download_and_save_tile(x, y, z, panoid)

    z = 5
    base_dir = path.join('raw', f'z{z}', '_'.join(panoid))
    if redownload_existing or not path.isdir(base_dir):
        makedirs(base_dir, exist_ok=True)

        # for y in range(int(2**max(0, z-1))):
        for y in range(7, 10):
            with Pool(32) as p:
                args = [(c[0], *c[1]) for c in zip([b for b in range(32)], [[y, z, panoid]]*32)]

                p.map(download_and_save_tile, args)
            # for x in range(int(2**z)):
            #     download_and_save_tile(x, y, z, panoid)

for i, user_panoid in enumerate(user_panoids):
    print(f'{i+1}/{len(user_panoids)}')

    z = 4
    base_dir = path.join('raw', f'z{z}', '_'.join(user_panoid))
    if redownload_existing or not path.isdir(base_dir):
        makedirs(base_dir, exist_ok=True)

        # for y in range(int(2**max(0, z-1))):
        for y in range(2, 6):
            with Pool(14) as p:
                args = [(c[0], *c[1]) for c in zip([b for b in range(14)], [[y, z, user_panoid]]*14)]

                p.map(download_and_save_user_tile, args)
            # for x in range(14):
            #     download_and_save_user_tile(x, y, z, user_panoid)