# :coding: utf-8

import os

from flask import Flask, request

import synes

app = Flask(__name__, static_folder="../static", static_url_path="/")


@app.route("/")
def index():
    return app.send_static_file("index.html")
    # return "<h1>Foo</h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=os.getenv("PORT", 80))
