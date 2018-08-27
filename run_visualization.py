import os
import fnmatch
import re
import numpy as np
from PIL import Image
import uuid
import matplotlib.image as image
from matplotlib.colors import LinearSegmentedColormap
from flask import Flask, send_from_directory, render_template, jsonify, request
from attgan.my_util import get_result
from util import *

import os
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



@app.route('/images')
def get_images( ):
    input_image = "static/img/0.png"
    atts = None
    level = None

    if atts is not None:
       input_image = atts[0]

    image_atts =  get_result(input_image,atts,level)









if __name__ == '__main__':
    app.run("127.0.0.1", port=8000, debug=True)
