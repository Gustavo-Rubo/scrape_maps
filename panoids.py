import requests
import numpy as np
import json

panoids = []

with open('sample.har', 'r') as f:
    data = json.loads(f.read())

for entry in data['log']['entries']:
    if entry['response']['content']['text'][4:] != '':
        res = json.loads(entry['response']['content']['text'][4:])
        for b in res[0]:
            if len(b[0]) == 22:
                panoid = (b[0], *b[8][0][1:])
            # elif len(b[9]) == 22:
            #     panoid = b[9]
            print(panoid)
            panoids.append(panoid)

print(len(list(set(panoids))))
np.save('panoids', list(set(panoids)))