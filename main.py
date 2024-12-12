import threading

import cv2

from gui.ttk import GUI, SetupButtons, SetupLayout
from model.capture import VideoCapture
from model.yolo import DetectObjects, DoNothing
from visual.compare import CompareNoise

state = {
    "isCapturing": True,
    "isDetecting": True,
    "isComparing": True,
    "priority": {
        "high": (200, 200, 400, 300),
        "medium": (100, 100, 200, 150),
    },
    "interval": 1,
    "priorityThreshold": {
        "high": 10,
        "medium": 20,
        "low": 30,
    },
}


# Main entry point
def main():
    root = GUI()
    main, controlPanel, videoLabel = SetupLayout(root)

    SetupButtons(root, controlPanel)

    capture = cv2.VideoCapture(0)

    if not capture.isOpened():
        raise IOError("Cannot open webcam")

    compare_thread = threading.Thread(
        target=lambda: CompareNoise(capture, state),
        daemon=True,
    )
    compare_thread.start()

    video_thread = threading.Thread(
        target=lambda: VideoCapture(capture, root, DoNothing, videoLabel),
        daemon=True,
    )
    video_thread.start()

    root.mainloop()


if __name__ == "__main__":
    main()
