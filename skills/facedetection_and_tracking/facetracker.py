from flask import Flask, Response
from picamera2 import Picamera2
import cv2
import mediapipe as mp
import time
from gpiozero import AngularServo
import os

os.chdir("/home/colecodes/projects/Pico/motor_files") # make auto .lgd files stored in specific folder

# Webserver init
server = Flask(__name__)

# Facedetection model init
model = mp.solutions.face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

def detect_face_and_draw(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convert frame to rgb for model

    results = model.process(rgb_frame) # predict if face on frame

    # If face on frame
    if results.detections:
        height, width = frame.shape[:2] # frame.shape (height, width, color channels (B, G, R)) -> [:2] 640, 480 pixels

        # Loop through each detected face in frame and draw box
        for detected_face in results.detections:

            # Virtual box around face
            box = detected_face.location_data.relative_bounding_box # (xmin, ymin) -> 0 to 1, (height, width). (0, 0) is xmin, ymin

            # Top left corner
            x = int(box.xmin * width) # left edge
            y = int(box.ymin * height) # top edge, y increases downwards
            top_left = (x, y)

            # Width & height of box
            bounding_box_width = int(box.width * width)
            bounding_box_height = int(box.height * height)
            bottom_right = (x + bounding_box_width, y + bounding_box_height)

            cv2.rectangle(frame, top_left, bottom_right, color=(255, 255, 255), thickness=2)

    return frame

# Servo init
PIN = 21
servo = AngularServo(PIN)
servo = None

# Camera init
cam = Picamera2()
config = cam.create_preview_configuration(main={"size": (640, 480)})
cam.configure(config)
cam.start()

def frames_generator():
    while True:
        frame = cam.capture_array() # get one single frame from cam
        frame = detect_face_and_draw(frame)
        _, jpeg = cv2.imencode(".jpg", frame) # convert frame to jpeg
        yield (b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n") # send frame and pause here
    
@server.route("/")    
def video():
    return Response(frames_generator(), mimetype="multipart/x-mixed-replace; boundary=frame") # continously stream frames gen

# run
if __name__ == '__main__':
    server.run(host="0.0.0.0", port=5000, threaded=True)

"""
STEPS:
- Imports and initial setup [X]
- Implement live video feed using flask [X]
- Implement facedetection us mediapipe model and draw border [ ] *
- Track border positions (corners) [ ]
- Move camera with servo until face is in the middle (horizontal) of the screen [ ]
- Smooth out movements [ ]
- Thread and integrate with main loop [ ]
"""