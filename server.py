from flask import Flask, Response, render_template
from skills.motion import attach_motor, run_motor_forward, run_motor_backward, stop_motor
from picamera2 import Picamera2
from libcamera import Transform
import atexit
import time
import cv2
from robot import main

# Webpage
server = Flask(__name__)

# Camera setup
camera = None
def get_camera():
    global camera

    if camera is None:

        camera = Picamera2()
        config = camera.create_preview_configuration(
            main={"size": (640, 480), "format": "BGR888"}, # window size and channel
            transform=Transform(hflip=True, vflip=False) # flip window
        )
        camera.configure(config)
        camera.start()
        time.sleep(0.2) # quick warmup before starting server

    return camera

@server.route("/")
def index():
    """
    This function loads all if the html code.
    """
    return render_template("server.html")

def get_frames():
    """
    This function loads a bunch of frames creating a live video stream.
    """
    cam = get_camera()

    while True:
        frame = cam.capture_array()
        ok, buf = cv2.imencode('.jpg', frame)
        if not ok:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               buf.tobytes() + b'\r\n')

@server.route("/video")
def video():
    """
    This function loads the live video stream onto the webpage.
    """
    return Response(get_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@server.route("/forward")
def forward():
    """
    This function loads a button onto the webpage that moves the robot motor forward.
    """
    motor = attach_motor()
    run_motor_forward(motor)
    time.sleep(0.05)
    stop_motor(motor)

@server.route("/backward")
def backward():
    """
    This function loads a button onto the webpage that moves the robot motor backward.
    """
    motor = attach_motor()
    run_motor_backward(motor)
    time.sleep(0.05)
    stop_motor(motor)

@atexit.register
def cleanup():
    global camera
    try:
        if camera:
            camera.stop()
    except Exception:
        pass

def run_server():
    """
    This function starts the webpage server.
    """

    server.run(host="0.0.0.0", port=5000, threaded=True, use_reloader=False, debug=True)

if __name__ == '__main__':
    run_server()