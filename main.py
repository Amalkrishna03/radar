import threading

from gui.ttk import GUI, SetupButtons, SetupLayout
from model.yolo import ObjectDetectionModel
from model.capture import VideoCapture


# Main entry point
def main():
    root = GUI()
    main, controlPanel, videoLabel = SetupLayout(root)

    SetupButtons(root, controlPanel)

    objectDetectionData = ObjectDetectionModel()

    # Start video capture in a separate thread
    video_thread = threading.Thread(
        target=lambda: VideoCapture(root, objectDetectionData, videoLabel), 
        daemon=True
    )
    video_thread.start()

    root.mainloop()


if __name__ == "__main__":
    main()
