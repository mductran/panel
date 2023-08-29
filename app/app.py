from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from app.form import SearchForm

import os
import base64
from urllib.request import urlopen
import numpy as np

search_app = Flask(__name__)

# TODO: use environment variable
DBUSER = 'panels_user'
DBPASS = ''
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'panels'
SECRET_KEY = os.urandom(32)

search_app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)
search_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
search_app.config["SECRET_KEY"] = SECRET_KEY

db = SQLAlchemy(search_app)


@search_app.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm(request.form)

    if form.validate_on_submit:
        print("form submitted")

        print(form.picture.data)
        print(form.url.data)

        if form.picture.data:
            print("user upload image")
            img = form.picture.data
            _, buffer = cv2.imencode('.jpg', img)
            buffer = base64.b64encode(buffer)
            return render_template("result.html", image=buffer)
        elif form.url.data:
            print(f"user upload url: {form.url.data}")
            response = urlopen(form.url.data)
            img = np.array(bytearray(response.read()), dtype=np.uint8)
            return render_template("result.html", image=img)
    return render_template("index.html")


@search_app.route("/result", methods=["GET"])
def result():
    image = request.args["image"]
    print(image)
    return render_template("result.html")
