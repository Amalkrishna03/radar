import time
import threading
import cv2

from visual.preprocessing import FindVisualDifference, PreprocessFrame, ExtractPriority
from utils.state import LiveState, State

listPriorityKeys = ["low", "medium", "high"]

limit = 70


def CompareAction(
    old: cv2.typing.MatLike,
    new: cv2.typing.MatLike,
    threshold: int,
    action: callable,
):
    thread = threading.Thread(
        target=lambda: action(FindVisualDifference(old, new, threshold)),
        daemon=True,
    )
    thread.start()


def CompareNoise(capture, state:State, liveState:LiveState, actions: dict[str, callable]):
    oldFrame = None
    
    def createStopper(action):
        def actionWithStopper(value):
            action(value)
            if value >= limit:
                liveState["isComparing"] = False
                liveState["isDetecting"] = True
                liveState["isSaving"] = True
                
            
        return actionWithStopper

    while liveState["isComparing"]:
        ret1, frameNew = capture.read()
        if not ret1:
            capture.release()
            raise IOError("Failed to capture new frame")

        grayNew = PreprocessFrame(frameNew)

        copy, high = ExtractPriority(grayNew, state["priority"]["high"])
        low, medium = ExtractPriority(copy, state["priority"]["medium"])

        newFrame = {
            "low": low,
            "medium": medium,
            "high": high,
        }

        if oldFrame is not None:
            [
                CompareAction(
                    oldFrame[key],
                    newFrame[key],
                    state["priorityThreshold"][key],
                    createStopper(actions[key])
                )
                for key in listPriorityKeys
            ]

        time.sleep(state["interval"])
        oldFrame = newFrame
