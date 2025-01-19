import threading

import cv2

from main import main
from stream import main as stream

if __name__ == "__main__":
    capture = cv2.VideoCapture(0)

    if not capture.isOpened():
        raise IOError("Cannot open webcam")
    
    main_thread = threading.Thread(
        target=lambda: main(capture),
        daemon=True,
    )
    main_thread.start()
    
    stream_thread = threading.Thread(
        target=lambda: stream(capture),
        daemon=True,
    )
    stream_thread.start()
    
    print("Threads started")
    
    main_thread.join()
    stream_thread.join()