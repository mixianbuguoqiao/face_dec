#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response
import cv2


Camera = import_module('camera.camera_' + "opencv").Camera

app = Flask(__name__)

global cropImg

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')




def gen(camera):
    """Video streaming generator function."""
    facecasc = cv2.CascadeClassifier('./static/haarcascade_files/haarcascade_frontalface_default.xml')

    while True:
        frame = camera.get_frame()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = facecasc.detectMultiScale(gray, 1.3, 5)
        if not len(faces) > 0:
           pass
        else:
            for face in faces:

                (x, y, w, h) = face

                middle_x = int(x + (w / 2))
                middle_y = int(y + (h / 2))


                if y + h - 5 > y + 10 and x + w - 10 > x + 10:
                    cropImg = frame[middle_y - 163: middle_y + 164 , middle_x - 133 : middle_x + 134]
                    cv2.imwrite("123.jpg",cropImg)
                else:
                    continue

                frame = cv2.rectangle(frame, (middle_x - 133, middle_y - 163), (middle_x + 134, middle_y + 164 ), (255, 0, 0), 2)


        frame = cv2.imencode('.jpg', frame)[1].tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':

    app.run(host='127.0.0.1', threaded=True)
