import threading

import cv2

from gui.ttk import GUI, SetupButtons, SetupGraphEqualizer, SetupLayout
from model.capture import VideoCapture
from model.vector import GetNow, SaveSituation
from model.vision import VisionModel
from model.yolo import DetectObjects, DoNothing, RenderFrameActions
from utils.state import LiveState, State
from utils.storage import SaveToBucket
from visual.canvas import DrawingApp
from visual.compare import CompareNoise
from visual.image import GetBase64
from visual.preprocessing import DrawWrapped

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
    base64, bytes = GetBase64(frame)

    text = VisionModel(base64)
    print(">", text)

    id = SaveSituation(text, time, {"label": label})

    SaveToBucket(bytes, id)


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
    main()

# from fastapi import FastAPI
# from fastapi.routing import APIRoute
# from starlette.middleware.cors import CORSMiddleware

# from api.main import api_router

# app = FastAPI(title="RADAR")
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# app.include_router(api_router, prefix="/api")
