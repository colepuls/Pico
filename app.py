from robot import main
from skills.facedetection_and_tracking.facetracker import face_tracker
import threading as thr

def start_robot():
    """
    This function starts the robot.
    - Threads the server and robot chat loop to run at the same time.
    """
    robot_loop_thread = thr.Thread(target=main)
    facetracker_thread = thr.Thread(target=face_tracker)
    robot_loop_thread.start()
    facetracker_thread.start()
    robot_loop_thread.join()
    facetracker_thread.join()

if __name__ == "__main__":
    start_robot()