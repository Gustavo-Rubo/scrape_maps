import requests
import numpy as np
import json
from os import path

panoids = np.array([])
if path.exists('panoids.npy'):
    panoids = list(np.load('panoids.npy'))

user_panoids = np.array([])
if path.exists('user_panoids.npy'):
    user_panoids = list(np.load('user_panoids.npy'))

with open('sample.har', 'r') as f:
    data = json.loads(f.read())

for entry in data['log']['entries']:
    if entry['response']['content']['text'][4:] != '':
        res = json.loads(entry['response']['content']['text'][4:])
        if res[0] is not None:
            for b in res[0]:
                if len(b[0]) == 22:
                    panoid = [b[0], *b[8][0][1:]]
                    # print(panoid)
                    if len(panoids) == 0:
                        panoids = np.array([panoid])
                    else:
                        panoids = np.append(panoids, [panoid], axis=0)
                else:
                    user_panoid = [b[0], *b[8][0][1:]]
                    if len(user_panoids) == 0:
                        user_panoids = np.array([user_panoid])
                    else:
                        user_panoids = np.append(user_panoids, [user_panoid], axis=0)
                # user submitted panoids are length 44 and they may go up to z4 resolution

print('panoids:', len(np.unique(panoids)))
print('user panoids:', len(np.unique(user_panoids)))
np.save('panoids', np.unique(panoids, axis=0))
np.save('user_panoids', np.unique(user_panoids, axis=0))