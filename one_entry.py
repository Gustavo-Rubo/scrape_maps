import csv
import easyocr
import numpy as np
# import pandas as pd
import PIL.ExifTags
from PIL import Image
from glob import glob
from shapely import wkt
from os import path, getenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app import db, Macro, Submacro, Micro, TimestampMixin

easyocr_reader = easyocr.Reader(['pt', 'en'])

# ler uma imagem
# origem = foto
# arquivo_original
# ocr
# lat
# long

files = glob('photos/*')


def ocr_pano(img):
    box1 = (0, 0, img.width//2, img.height)
    box2 = (img.width//2, 0, img.width, img.height)
    canvas_size = 2100

    easyocr_res = easyocr_reader.readtext(np.array(img.crop(box1)),
        batch_size=1, detail=0, text_threshold=.6, canvas_size=canvas_size)
    easyocr_res.extend(easyocr_reader.readtext(np.array(img.crop(box1).rotate(-90, expand=1)),
        batch_size=1, detail=0, text_threshold=.6, canvas_size=canvas_size))
    easyocr_res.extend(easyocr_reader.readtext(np.array(img.crop(box2)),
        batch_size=1, detail=0, text_threshold=.6, canvas_size=canvas_size))
    easyocr_res.extend(easyocr_reader.readtext(np.array(img.crop(box2).rotate(-90, expand=1)),
        batch_size=1, detail=0, text_threshold=.6, canvas_size=canvas_size))

    return easyocr_res

def ocr_photo(img):
    canvas_size = 2100

    easyocr_res = easyocr_reader.readtext(np.array(img),
        batch_size=1, detail=0, text_threshold=.6, canvas_size=canvas_size)
    easyocr_res.extend(easyocr_reader.readtext(np.array(img.rotate(-90, expand=1)),
        batch_size=1, detail=0, text_threshold=.6, canvas_size=canvas_size))

    return easyocr_res

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

for file in files[:1]:
    img = Image.open(file)
    origem = 'foto'
    arquivo_original = path.split(file)[-1]
    lat, long = get_lat_long(img)
    ocr = ocr_photo(img)

    micro = Micro(
        origem=origem,
        lat=lat,
        long=long,
        arquivo_original=arquivo_original,
        ocr='\n'.join(ocr),
    )
    db.session.add(micro)
    db.session.commit()

print('b')

# m_per_coord = 1e5

# map_file = path.join('data', 'mapa.csv')
# map_df = pd.read_csv(map_file)

# p = wkt.loads('POINT(-46.730618959754395 -23.556135026537184)')

# macros = []
# for index, row in map_df.dropna(how='all')[['WKT', 'name']].iterrows():
#     poly = wkt.loads(row['WKT'])
#     print(row['name'], poly.contains(p), poly.boundary.distance(p)*m_per_coord)