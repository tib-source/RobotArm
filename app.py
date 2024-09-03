import os
from flask import Flask, request, render_template

app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = os.path.join(os.getcwd(), "uploads")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if request.files:
        print(request.files)
        image = request.files["data"]
        path = os.path.join(app.config["IMAGE_UPLOADS"], image.filename)
        image.save(path)
        print(path)
        return path
