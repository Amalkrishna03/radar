import threading

import cv2

from gui.ttk import GUI, SetupButtons, SetupLayout, SetupGraphEqualizer
from model.capture import VideoCapture
from model.vision import VisionModel
from model.vector import GetNow, SaveSituation
from model.yolo import DetectObjects, DoNothing, RenderFrameActions
from visual.compare import CompareNoise
from visual.preprocessing import DrawWrapped
from utils.state import LiveState, State

state = State.get_instance()
print(state)

liveState: LiveState = {
    "isCapturing": True,
    "isDetecting": False,
    "isAnomaly": False,
    "isComparing": True,
    "isSaving": False,
}

def RunVisionModel(frame, label):
    time = GetNow()
    text = VisionModel(frame)
    print(">", text)
    SaveSituation(text, time, {"label": label})

observation = [DrawWrapped(state.data)]
understanding = [RunVisionModel]
detection = [DetectObjects(understanding, liveState)]

functionMap = {
    "observation": observation,
    "detection": detection,
    "understanding": understanding,
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
        target=lambda: CompareNoise(capture, liveState, threeGraphs),
        daemon=True,
    )
    compare_thread.start()

    video_thread = threading.Thread(
        target=lambda: VideoCapture(
            capture,
            root,
            lambda fm: RenderFrameActions(
                fm,
                functionMap["observation"]
                if (not liveState["isDetecting"])
                else functionMap["detection"],
            ),
            videoLabel,
        ),
        daemon=True,
    )
    video_thread.start()

    def startObjectDetection():
        if liveState["isDetecting"] is False:
            liveState["isDetecting"] = True

    def stopObjectDetection():
        if liveState["isDetecting"] is True:
            liveState["isDetecting"] = False

    SetupButtons(
        root,
        controlPanel,
        {
            "startObjectDetection": startObjectDetection,
            "stopObjectDetection": stopObjectDetection,
        },
    )

    root.mainloop()


if __name__ == "__main__":
    main()
