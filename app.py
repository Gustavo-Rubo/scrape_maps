import json
import base64
import numpy as np
from os import path
from flask import Flask, jsonify, request, render_template, send_from_directory

app = Flask(__name__)

with open('database.json', 'r') as f:
    db = json.load(f)
    db = np.array(db)


@app.route('/full_pano/<path:path>')
def send_pano(path):
    return send_from_directory('stitched/z5', path)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':

        data = request.json
        text = data['search']

        res = []
        if text != '':
            # TODO: better search function
            res = db[[str.lower(text) in str.lower(
                ' '.join(d['ocr'])) for d in db]]

            for r in res:
                with open(path.join('stitched', 'z1', r['thumb_file']), 'rb') as f:
                    thumb = f.read()
                    r['thumb_data'] = str(base64.b64encode(thumb))

        return jsonify(list(res))
