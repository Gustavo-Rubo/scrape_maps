
import csv
import pandas as pd
from os import path
from shapely import wkt

m_per_coord = 1e5

map_file = path.join('data', 'map.csv')
map_df = pd.read_csv(map_file)

p = wkt.loads('POINT(-46.730618959754395 -23.556135026537184)')

macros = []
for index, row in map_df.dropna(how='all')[['WKT', 'name']].iterrows():
    poly = wkt.loads(row['WKT'])
    print(row['name'], poly.contains(p), poly.boundary.distance(p)*m_per_coord)