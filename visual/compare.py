import time
import threading
import cv2

from visual.preprocessing import FindVisualDifference, PreprocessFrame, ExtractPriority


def CompareAction(
    old: cv2.typing.MatLike, new: cv2.typing.MatLike, threshold: int, title: str
):
    thread = threading.Thread(
        target=lambda: print(
            f"Visual difference in {title}: {FindVisualDifference(old, new, threshold)}%"
        ),
        daemon=True,
    )
    thread.start()


def CompareNoise(capture, state):
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
                    oldFrame[frame], newFrame[frame], state["priorityThreshold"][frame], frame
                )
                for frame in ["low", "medium", "high"]
            ]

        time.sleep(state["interval"])
        oldFrame = newFrame
