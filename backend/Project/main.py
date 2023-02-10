import json
import os
import os.path
from pathlib import Path
from flask import Flask, request, g, session

import chennai

app = Flask(__name__)
filename = "data.csv"
app.config['UPLOAD_PATH'] = 'static/files'


@app.route('/verifyUser', methods=['POST'])
def verify_user():
    if request.method == 'POST':

        data_1 = json.loads(request.data)
        if data_1['password'] == 'Gowshick':
            return {"result": True}
    return {"result": False}


@app.route('/files', methods=['GET', 'POST'])
def file():
    if request.method == 'POST':
        f = request.files['csv']
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        # data = request.form
        # print(data['test'])

        return {"result": True}
    return {"result": False}


@app.route('/house', methods=['GET', 'POST'])
def house():
    if request.method == "POST":
        data_1 = json.loads(request.data)
        area = data_1['area']
        builder = data_1['builder']
        sqft = data_1['sqft']
        bath = data_1['bath']
        bhk = data_1['bhk']
        year = data_1['year']
        path = 'static/files/data.csv'
        isdir = Path(path)
        if isdir.exists():
            # check if file exists
            price = chennai.predict_price(area, builder, sqft, bath, bhk, year, path)
            p = price
            # return eror response
            return {"Result": p}
    return {"Result": False}


@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']


if __name__ == "__main__":
    app.run(debug=True)
