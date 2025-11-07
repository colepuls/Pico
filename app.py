from robot import main
# from server import run_server
import threading as thr

def start_robot():
    """
    This function starts the robot.
    - Threads the server and robot chat loop to run at the same time.
    """
    pico_main_thread = thr.Thread(target=main)
    # pico_server_thread = thr.Thread(target=run_server)
    pico_main_thread.start()
    # pico_server_thread.start()
    pico_main_thread.join()
    # pico_server_thread.join()

if __name__ == "__main__":
    start_robot()