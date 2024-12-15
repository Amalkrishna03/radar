import threading

import cv2

from gui.ttk import GUI, SetupButtons, SetupLayout, SetupGraphEqualizer
from model.capture import VideoCapture
from model.yolo import DetectObjects, DoNothing, RenderFrameActions
from visual.compare import CompareNoise
from visual.preprocessing import DrawWrapped
from utils.state import state

internal = {
    "renderActions": [DoNothing, DrawWrapped(state)]
}


# Main entry point
def main():
    root = GUI()
    mainPanel, videoLabel, controlPanel, noisePanel, messagePanel = SetupLayout(root)
    threeGraphs = SetupGraphEqualizer(noisePanel)
       
    capture = cv2.VideoCapture(0)


    if not capture.isOpened():
        raise IOError("Cannot open webcam")

    compare_thread = threading.Thread(
        target=lambda: CompareNoise(capture, state, threeGraphs),
        daemon=True,
    )
    compare_thread.start()

    video_thread = threading.Thread(
        target=lambda: VideoCapture(
            capture,
            root,
            lambda fm: RenderFrameActions(fm, internal["renderActions"]),
            videoLabel,
            state
        ),
        daemon=True,
    )
    video_thread.start()
    
    def startObjectDetection(): 
        if state["isDetecting"] is False:
            state["isDetecting"] = True
        
    def stopObjectDetection(): 
        if state["isDetecting"] is True:
            state["isDetecting"] = False
    
    SetupButtons(root, controlPanel, {
        "startObjectDetection": startObjectDetection,
        "stopObjectDetection": stopObjectDetection,
    })

    root.mainloop()


if __name__ == "__main__":
    main()
