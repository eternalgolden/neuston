'''
    threads.py

    manages stuff about threads

'''
import threading
import time

exit_event = threading.Event()

def restore():

    while True:
        if exit_event.wait(timeout=5):
            break
        print("owo")


restore_timer = threading.Thread(target=restore)
restore_timer.daemon = True


def signal_handler(signum, frame):
    exit_event.set()
