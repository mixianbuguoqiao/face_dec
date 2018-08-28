import cv2

from importlib import import_module
Camera = import_module('camera.camera_' + "opencv").Camera
from attgan.my_util import get_result

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
def get_images():
    print('11111111111111111')
    input_image = "static/img/000001.jpg"
    atts = None
    level = None

    if atts is not None:
        input_image = atts[0]
    print(input_image,atts,level)
    image_atts = get_result(input_image, atts, level)
    print(image_atts)
    return '1'

# get_images()