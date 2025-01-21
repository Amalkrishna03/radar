import threading

import cv2

from gui.ttk import GUI, SetupButtons, SetupGraphEqualizer, SetupLayout
from model.capture import VideoCapture
from model.yolo import DetectObjects, DoNothing, RenderFrameActions
from utils.state import LiveState, State
from utils.situation import RunSaveSituation
from visual.canvas import DrawingApp
from visual.compare import CompareNoise
from visual.preprocessing import DrawWrapped

state = State.get_instance()

liveState: LiveState = {
    "isCapturing": True,
    "isDetecting": False,
    "isAnomaly": False,
    "isComparing": True,
    "isSaving": False,
}


# Main entry point
def main(capture: cv2.VideoCapture):
    print("Starting main")
    root = GUI()
    mainPanel, videoLabel, controlPanel, noisePanel, messagePanel, video1, video2 = (
        SetupLayout(root)
    )
    threeGraphs = SetupGraphEqualizer(noisePanel)

    observation = [DrawWrapped(state.data["priority"])]
    understanding = [RunSaveSituation]
    detection = [DetectObjects(understanding, liveState)]

    functionMap = {
        "observation": observation,
        "detection": detection,
        "understanding": understanding,
    }

    # capture = cv2.VideoCapture(0)

    # if not capture.isOpened():
    #     raise IOError("Cannot open webcam")

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

    def EditPriority(priority: str):
        def code():
            canvas_thread = threading.Thread(
                target=lambda: DrawingApp(priority),
                daemon=True,
            )
            canvas_thread.start()

        return code

    SetupButtons(
        controlPanel,
        {
            "Quit": root.quit,
            "Start_Object_Detection": startObjectDetection,
            "Stop_Object_Detection": stopObjectDetection,
            "Edit_Priority_High": EditPriority("high"),
            "Edit_Priority_Medium": EditPriority("medium"),
        },
    )

    root.mainloop()


if __name__ == "__main__":
    capture = cv2.VideoCapture(0)
    if not capture.isOpened():
        raise IOError("Cannot open webcam")

    main(capture)