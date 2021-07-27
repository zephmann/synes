# :coding: utf-8

import datetime
import os

from flask import Flask, request, url_for
from werkzeug.utils import secure_filename

import synes

IMAGE_EXTENSIONS = (".png", ".jpg")
AUDIO_EXTENSIONS = (".wav",)
ALLOWED_EXTENSIONS = IMAGE_EXTENSIONS + AUDIO_EXTENSIONS
UPLOAD_FOLDER = os.path.abspath("./tmp/")
UPLOAD_README = "readme.txt"
REMOVE_AGE = 60

app = Flask(__name__, static_folder="../../static", static_url_path="/")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def index():
    _cleanup_upload_directory()

    return app.send_static_file("index.html")


@app.route('/upload', methods=["POST"])
def upload():
    _cleanup_upload_directory()

    # get and validate upload file
    if "upload" not in request.files:
        return "No file in request."

    upload_file = request.files["upload"]
    filename = upload_file.filename
    if not filename:
        return "User did not select a file."

    filename = secure_filename(filename)

    _, ext = os.path.splitext(filename)
    if ext not in ALLOWED_EXTENSIONS:
        return "Unsupported file type '{}'.".format(ext)

    # get and validate dimension value
    if "dimension" not in request.form:
        return "Dimension is missing from form."

    # TODO ensure value can be converted to int?
    translate_dimension = int(request.form["dimension"])

    # TODO generate temp hash for file to prevent clashes
    saved_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    upload_file.save(saved_filepath)

    if ext in IMAGE_EXTENSIONS:
        output_filepath = synes.translate_image(
            saved_filepath, translate_dimension
        )

    else:
        output_filepath = synes.translate_audio(
            saved_filepath, translate_dimension
        )

    return (
        "Saved to {}\nTranslated to <a href=\"{}\">test!</a>".format(saved_filepath, output_filepath)
    )


def _cleanup_upload_directory():
    start = datetime.datetime.now()
    for upload_file in os.listdir(UPLOAD_FOLDER):
        if upload_file == UPLOAD_README:
            continue

        filepath = os.path.join(UPLOAD_FOLDER, upload_file)
        ctime = datetime.datetime.fromtimestamp(os.path.getctime(filepath))
        time_diff = start - ctime

        if time_diff.days or time_diff.seconds > REMOVE_AGE:
            print("Removing old temp file {}".format(filepath))
            os.remove(filepath)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=os.getenv("PORT", 80))
