from flask import Flask, Response, render_template_string
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

server = Flask(__name__)
HTML = """
<!doctype html>
<title>Pico Server</title>
<style>
    body{margin:0;background:#111;display:flex;justify-content:center;align-items:center;height:100vh}
    img{max-width:98vw;max-height:98vh}
</style>
<img src="/video" alt="video">
"""

@server.route("/")
def index():
    return render_template_string(HTML)

def get_frames():
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
    return Response(get_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def run_server():
    server.run(host="0.0.0.0", port=5000, threaded=True, use_reloader=False, debug=False)

