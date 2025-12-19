from flask import Flask, Response
from picamera2 import Picamera2
import cv2
import mediapipe as mp
import time
from gpiozero import AngularServo
import os; os.chdir("/home/colecodes/projects/Pico/motor_files")

# Webserver init
server = Flask(__name__)

# Servo init
servo = AngularServo(21,  min_angle=-90, max_angle=90, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)
servo.angle = None
angle = 0.0
last_update = 0.0

# Facedetection model init
model = mp.solutions.face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

# Camera init
cam = Picamera2()
config = cam.create_preview_configuration(main={"size": (640, 480)})
cam.configure(config)
cam.start()

def detect_face_and_track(frame):

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convert frame to rgb for model

    results = model.process(frame) # predict if face on frame

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

            # Get center of face box
            box_center_x = x + bounding_box_width // 2

            # Get center of frame
            frame_center_x = width // 2

            # Draw
            cv2.rectangle(frame, top_left, bottom_right, color=(255, 255, 255), thickness=2) # face box
            cv2.line(frame, (box_center_x, 0), (box_center_x, height), color=(0, 0, 255), thickness=1) # center of face box
            # Deadzone
            cv2.line(frame, (frame_center_x + 100, 0), (frame_center_x + 100, height), color=(0, 255, 0), thickness=2)
            cv2.line(frame, (frame_center_x - 100, 0), (frame_center_x - 100, height), color=(0, 255, 0), thickness=2)

            # Track face with servo
            track_face(frame_center_x, box_center_x)

    return frame

# NOTE: Current issue: 
#           When distance from target area is short, the calculated degree is to small causing the servo not to move far enough.
#           When distance is long, the opposite happens, causing servo to overshoot
# Fix: Tweak step depending on calculated error
def track_face(frame_center, box_center):
    global last_update, angle
    now = time.time()

    if now - last_update <= 1:
        servo.angle = None
        return

    error = box_center - frame_center # distance from center in pixels

    if abs(error) < 100:
        servo.angle = None
        return
        
    step = 2.0 # degrees multiplier
    degrees = -(error / frame_center) * step # normalize then convert to degrees
    angle += degrees
    angle = max(-10, min(10, angle)) # clamp to prevent over shooting
    servo.angle = angle # update angle
    last_update = now
    
def frames_generator():
    while True:
        frame = cam.capture_array() # get one single frame from cam
        frame = detect_face_and_track(frame)
        _, jpeg = cv2.imencode(".jpg", frame) # convert frame to jpeg
        yield (b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n") # send frame and pause here
    
@server.route("/")    
def video():
    return Response(frames_generator(), mimetype="multipart/x-mixed-replace; boundary=frame") # continously stream frames gen

# Threaded func inside app.py
def face_tracker():
    server.run(host="0.0.0.0", port=5000, threaded=True)

# run
if __name__ == '__main__':
    server.run(host="0.0.0.0", port=5000, threaded=True)