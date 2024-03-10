from glob import glob
from os import path, rename, listdir
import shutil
import numpy as np

panoids = np.load('panoids.npy')
panoids = np.append(panoids, np.load('user_panoids.npy'), axis=0)

for panoid in panoids:
    for z in [1, 4, 5]:
        # raw
        path_og = path.join('raw', f'z{z}', '_'.join(panoid))
        path_new = path.join('raw', f'z{z}', '='.join(panoid))

        try:
            for file in listdir(path_og):
                shutil.move(path.join(path_og, file), path.join(path_new, file))
        except:
            print(z, 'filenotfound')
        # rename(path_og, path_new)

        # stitched
        path_og = path.join('stitched', f'z{z}', '_'.join(panoid))+'.jpeg'
        path_new = path.join('stitched', f'z{z}', '='.join(panoid))+'.jpeg'
        try:
            rename(path_og, path_new)
        except:
            print(z, 'filenotfound')
