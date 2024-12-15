import time
import threading
import cv2

from visual.preprocessing import FindVisualDifference, PreprocessFrame, ExtractPriority
from utils.state import State

listPriorityKeys = ["low", "medium", "high"]


def CompareAction(
    old: cv2.typing.MatLike,
    new: cv2.typing.MatLike,
    threshold: int,
    title: listPriorityKeys,
    action: callable,
):
    thread = threading.Thread(
        target=lambda: action(FindVisualDifference(old, new, threshold)),
        daemon=True,
    )
    thread.start()


def CompareNoise(capture, state:State, actions: dict[listPriorityKeys, callable]):
    oldFrame = None

    while state["isComparing"]:
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
                    key,
                    actions[key]
                )
                for key in listPriorityKeys
            ]

        time.sleep(state["interval"])
        oldFrame = newFrame
