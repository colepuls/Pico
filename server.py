from flask import Flask, Response, render_template_string
from skills.motion import attach_motor, run_motor_forward, run_motor_backward, stop_motor
from picamera2 import Picamera2
from libcamera import Transform
import numpy as np
import time
import cv2

# Initialize camera
camera = Picamera2()
config = camera.create_preview_configuration(
    main={"size": (640, 480), "format": "BGR888"}, # window size and channel
    transform=Transform(hflip=True, vflip=True) # flip window
)
camera.configure(config)
camera.start()
time.sleep(0.2) # quick warmup before starting server

# Webpage
server = Flask(__name__)
HTML = """
<!doctype html>
<title>Pico Server</title>
<style>
    body{margin:0;background:#111;display:flex;flex-direction:column;align-items:center;justify-content:center;height:100vh;}
    img{max-width:90vw;max-height:70vh;}
    button{
        background-color:#fff;
        color:#000;
        border:none;
        padding:10px 20px;
        margin:10px;
        border-radius:8px;
        cursor:pointer;
        font-size:18px;
    }
    button:hover{background-color:#ddd;}
</style>

<img src="/video" alt="video">
<div>
  <button onclick="fetch('/forward')">→ Forward</button>
  <button onclick="fetch('/backward')">← Backward</button>
</div>
"""

@server.route("/")
def index():
    """
    This function loads all if the html code.
    """
    return render_template_string(HTML)

def get_frames():
    """
    This function loads a bunch of frames creating a live video stream.
    """
    while True:
        frame = camera.capture_array()
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

def run_server():
    """
    This function starts the webpage server.
    """
    server.run(host="0.0.0.0", port=5000, threaded=True, use_reloader=False, debug=False)

