import os
import subprocess
from flask_cors import CORS

from flask import Flask, request, render_template, send_from_directory
from BrachioGraph.brachiograph import BrachioGraph
from BrachioGraph.linedraw import image_to_json

app = Flask(__name__)
CORS(app)

app.config["IMAGE_UPLOADS"] = "./BrachioGraph/images"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def uploadAndDraw():
    if request.files:
        app.logger.debug(request.files)
        image = request.files["data"]
        path = os.path.join(app.config["IMAGE_UPLOADS"], image.filename)
        image.save(path)
        vectorise(image.filename.split(".")[0])
        return image.filename

    else:
        print(request)
        return


def vectorise(file_name):

    code = """
from linedraw import vectorise
vectorise("{}", draw_contours=2, draw_hatch=16)
    """
    # Change the current working directory to the target directory
    os.chdir("BrachioGraph/")
    subprocess.call(["python3", "-c", code.format(file_name)])
    os.chdir("../")


@app.route("/images/<path:name>")
def download_file(name):
    return send_from_directory(app.config["IMAGE_UPLOADS"], name)


def start_drawing(filename):
    # A "naively" calibrated plotter definition. We assume the default 10ms
    # pulse-width difference = 1 degree of motor movement. If the arms appear to
    # move in the wrong directions, try reversing the value of servo_1_degree_ms
    # and/or servo_2_degree_ms.

    bg = BrachioGraph(
        # the lengths of the arms
        inner_arm=8,
        outer_arm=8,
        # the drawing area
        bounds=(-6, 4, 6, 12),
        # relationship between servo angles and pulse-widths
        servo_1_degree_ms=-10,
        servo_2_degree_ms=10,
        # pulse-widths for pen up/down
        pw_down=1200,
        pw_up=1850,
    )

    # Vectorise the image
    image_to_json(filename, draw_contours=2, draw_hatch=16)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
