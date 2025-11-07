from main import main
# from server import run_server
import threading as thr

if __name__ == "__main__":
    pico_main_thread = thr.Thread(target=main)
    # pico_server_thread = thr.Thread(target=run_server)
    pico_main_thread.start()
    # pico_server_thread.start()
    pico_main_thread.join()
    # pico_server_thread.join()