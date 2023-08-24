import requests
import shutil
import numpy as np
from os import path, makedirs
from multiprocessing import Pool

redownload_existing = False


# panoids = ['eTPYmbok7Ho94LG2bW9XgA', 'tQbB6SQ_anc7hOUEJNxHfg', 'Bpw-92VrITn2LIim3gzlZw', 'wS2g9Ay4DqTuOPOQ5fPErg']
panoids = np.load('panoids.npy')
user_panoids = np.load('user_panoids.npy')

def download_and_save_tile(args):
    url = args[0]
    path = args[1]
    img = requests.get(url, stream=True)

    if img.status_code == 200:
        with open(path, 'wb') as f:
            shutil.copyfileobj(img.raw, f)
    else:
        print(img.status_code, path)


for i, panoid in enumerate(panoids):
    print(f'{i+1}/{len(panoids)}')

    base_streetview_url = 'https://streetviewpixels-pa.googleapis.com/v1/tile?cb_client=maps_sv.tactile'
    
    z = 1
    base_dir = path.join('raw', f'z{z}', '_'.join(panoid))
    if redownload_existing or not path.isdir(base_dir):
        makedirs(base_dir, exist_ok=True)
        for y in [0]:
            with Pool(2) as p:
                args = [
                    [base_streetview_url + f'&panoid={panoid[0]}&x={x}&y={y}&zoom={z}&nbt=1&fover=2',
                     path.join(base_dir, f'z{z}-y{y:02}-x{x:02}.jpeg')] for x in range(2)]
                p.map(download_and_save_tile, args)

    z = 5
    base_dir = path.join('raw', f'z{z}', '_'.join(panoid))
    if redownload_existing or not path.isdir(base_dir):
        makedirs(base_dir, exist_ok=True)
        for y in range(7, 10):
            with Pool(32) as p:
                args = [
                    [base_streetview_url + f'&panoid={panoid[0]}&x={x}&y={y}&zoom={z}&nbt=1&fover=2',
                     path.join(base_dir, f'z{z}-y{y:02}-x{x:02}.jpeg')] for x in range(32)]
                p.map(download_and_save_tile, args)


for i, user_panoid in enumerate(user_panoids):
    print(f'{i+1}/{len(user_panoids)}')

    base_url = 'https://lh3.ggpht.com/p/'

    z = 1
    base_dir = path.join('raw', f'z{z}', '_'.join(user_panoid))
    if redownload_existing or not path.isdir(base_dir):
        makedirs(base_dir, exist_ok=True)
        for y in [0]:
            with Pool(2) as p:
                args = [
                    [base_url + f'{user_panoid[0]}=x{x}-y{y}-z{z}',
                     path.join(base_dir, f'z{z}-y{y:02}-x{x:02}.jpeg')] for x in range(2)]       
                p.map(download_and_save_tile, args)
    
    z = 4
    base_dir = path.join('raw', f'z{z}', '_'.join(user_panoid))
    if redownload_existing or not path.isdir(base_dir):
        makedirs(base_dir, exist_ok=True)
        for y in range(2, 6):
            with Pool(14) as p:
                args = [
                    [base_url + f'{user_panoid[0]}=x{x}-y{y}-z{z}',
                     path.join(base_dir, f'z{z}-y{y:02}-x{x:02}.jpeg')] for x in range(32)]
                p.map(download_and_save_tile, args)