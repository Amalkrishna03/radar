import threading

import cv2

from software import main as software
from stream import main as stream

if __name__ == "__main__":
    capture = cv2.VideoCapture(0)

    if not capture.isOpened():
        raise IOError("Cannot open webcam")
    
    software_thread = threading.Thread(
        target=lambda: software(capture),
        daemon=True,
    )
    software_thread.start()
    
    stream_thread = threading.Thread(
        target=lambda: stream(capture),
        daemon=True,
    )
    stream_thread.start()
    
    print("Threads started")
    
    software_thread.join()
    stream_thread.join()
    
# uv run ./main.py