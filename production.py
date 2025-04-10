import cv2
import uvicorn
from fastapi.responses import StreamingResponse
import threading
import time

from model.capture import VideoCapture
from model.yolo import DoNothing, RunYolo, RunYoloSimple
from server import app
from server import main as MainServer
from utils.situation import RunSaveSituation
from utils.state import LiveState, State
from utils.file import WriteCapture
from utils.thread import StarterThread, RemoveThread
from visual.canvas import DrawingApp
from visual.compare import CompareNoise
from visual.image import ImageToStreamBytes
from visual.preprocessing import DrawWrapped
from visual.compare import listPriorityKeys

isStreaming = True

state = State.get_instance()

liveState: LiveState = {
    "isCapturing": True,  # camara feed input
    "isDetecting": False,  # yolo
    "isAnomaly": False,
    "isComparing": True,  # pixel comparison
    "isSaving": False,  # video save
}


@app.get("/live/start_stream")
async def start_stream():
    global isStreaming
    isStreaming = True
    return {"status": "started"}


@app.get("/live/stop_stream")
async def stop_stream():
    global isStreaming
    isStreaming = False
    return {"status": "stopped"}


def InstantaniousFrame(capture: cv2.VideoCapture):
    success, frame = capture.read()
    if not success:
        pass

    return frame


def DetectLoop(capture: cv2.VideoCapture):
    print("> Detecting", liveState["isDetecting"])
    while liveState["isDetecting"] is True:
        success, frame = capture.read()
        if not success:
            break

        RunYolo(liveState)(frame)

        time.sleep(state.data["interval"])


def DecisionLoop(capture: cv2.VideoCapture):
    while True:
        if liveState["isComparing"] is False:
            if RemoveThread("compare_thread"):
                print("> Comparison stopped")

            if liveState["isDetecting"] is True:
                StarterThread(
                    target=lambda: DetectLoop(capture),
                    name="detect_thread",
                )

            else:
                RemoveThread("detect_thread")

            if liveState["isAnomaly"] is True:

                def worker():
                    print("> Vision Running")
                    RunSaveSituation(InstantaniousFrame(capture), liveState)
                    liveState["isAnomaly"] = False

                StarterThread(
                    target=worker,
                    name="vision_thread",
                )

            else:
                RemoveThread("vision_thread")

            if liveState["isSaving"] is True:
                StarterThread(
                    target=lambda: WriteCapture(capture, liveState),
                    name="write_thread",
                )

            else:
                RemoveThread("write_thread")

        else:
            StarterThread(
                target=lambda: CompareNoise(
                    capture,
                    liveState,
                    {
                        "low": lambda value: print("Low", value),
                        "medium": lambda value: print("Medium", value),
                        "high": lambda value: print("High", value),
                    },
                ),
                name="compare_thread",
            )

        time.sleep(state.data["interval"])


def DecisionThread(capture: cv2.VideoCapture):
    decision_thread = threading.Thread(
        target=lambda: DecisionLoop(capture),
        daemon=True,
    )
    decision_thread.start()


def main(capture: cv2.VideoCapture):
    print("Starting stream")

    def generate_frames():
        global isStreaming
        SimpleYoloCode = RunYoloSimple()

        while isStreaming:
            success, frame = capture.read()
            if success:
                if liveState["isDetecting"]:
                    newFrame = SimpleYoloCode(frame)
                else:
                    newFrame = frame

                streamData = ImageToStreamBytes(newFrame)
                if streamData:
                    yield streamData

    @app.get("/live/stream")
    async def video_feed():
        return StreamingResponse(
            generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame"
        )

    MainServer()
    DecisionThread(capture)

    # @app.lifespan("/live/shutdown")
    # async def shutdown_event():
    #     if capture.isOpened():
    #         capture.release()

    uvicorn.run(app, host="0.0.0.0", port=4000)


if __name__ == "__main__":
    capture = cv2.VideoCapture(0)
    if not capture.isOpened():
        raise IOError("Cannot open webcam")

    main(capture)

# uv run stream.py
