#!/usr/bin/env
from flask import Flask, render_template, Response, request
import io
import cv2
import time

time1 = []
time2 = []
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
vc = cv2.VideoCapture(0)
app = Flask(__name__)#template_folder='templates'

def t():
    time.sleep(1)
    return 1


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    Sec1 = 0
    Sec2 = 0
    Min2 = 0
    Min1 = 0

    """Video streaming generator function."""

    while True:
        read_return_code, frame = vc.read()  # Read Video frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # frame into  gray image
        face_rects = face_cascade.detectMultiScale(gray, 1.3, 3)

        for (x, y, w, h) in face_rects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        print(face_rects)
        if len(face_rects) > 0:  # Face on Screen Time
            Sec1 +=(1/6)
            print(str(Min1) + " Mins " + str(Sec1) + " Sec ")
            cv2.putText(frame, "Time: " + str(Min1) + " Mins " + str(int(Sec1)) + " Sec ", (0, frame.shape[0] - 30),
                        cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 255), 1)
            cv2.putText(frame, "No. of  face Dected " + str(face_rects.shape[0]), (0, frame.shape[0] - 10),
                        cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 255), 1)
            if int(Sec1) == 60:
                Sec1 = 0
                Min1 += 1
                # print(str(Min1) + " Minute")

        else:  # Face Not on Screen Time
            Sec2 += (1/6)
            cv2.putText(frame, "Time: " + str(Min2) + " Mins " + str(int(Sec2)) + " Sec ", (0, frame.shape[0] - 40),
                        cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 255, 255), 1)
            if int(Sec2) == 60:
                Sec2 = 0
                Min2 += 1
                # print(str(Min1) + " Minute")
                time2.append(Min2)

        encode_return_code, image_buffer = cv2.imencode('.jpg', frame)
        io_buf = io.BytesIO(image_buffer)
        yield b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + io_buf.read() + b'\r\n'


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/quit')
def quit_():
    cv2.waitKey(0)
    vc.release()
    return "<html><h1>Prepared By Ritik Chhipa</h1></html>"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
