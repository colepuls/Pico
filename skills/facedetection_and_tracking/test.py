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
facedetection = mp.solutions.face_detection

# Servo init
PIN = 21
servo = AngularServo(PIN)

# Camera init
cam = Picamera2()
config = cam.create_preview_configuration(main={"size": (640, 480)})
cam.configure(config)
cam.start()

frame = cam.capture_array()