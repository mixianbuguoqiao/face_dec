import os
import fnmatch
import re
import numpy as np
from PIL import Image
import uuid
import matplotlib.image as image
from matplotlib.colors import LinearSegmentedColormap
from flask import Flask, send_from_directory, render_template, jsonify, request

from util import get_result,gen,Camera
import json


from flask import Flask, render_template, Response

app = Flask(__name__)


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/")
def index():


    return render_template('index.html')


@app.route('/images', methods=['POST', 'GET'])
def get_images():
    data = json.loads(request.form['data'])  ####{'input_image': '000001.jpg', 'atts': ['Beard', 'Old'], 'level': [0.4, -0.6]}


    input_image = data["input_image"]
    atts = data["atts"]
    level = data["level"]
    print(input_image,atts,level)


    if atts is not None:
         image_atts = get_result("static/img/"+input_image)
         print(image_atts)



    get_result("static/img/"+input_image, test_atts=atts, test_ints=level)

    return '1'


if __name__ == '__main__':
    # get_images()

    app.run("127.0.0.1", port=8000,debug=True)
