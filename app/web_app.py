# :coding: utf-8

from flask import Flask, render_template

import synes

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")
