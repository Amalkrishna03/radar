import asyncio
import threading

import numpy as np
from typing import List, Callable
from ultralytics import YOLO
from utils.state import LiveState, State

model_name: str = "yolov8n.pt"
model = YOLO(model_name)


def DetectObjects(listOfFunctions: List[Callable], liveState: LiveState):
    data = State.get_instance().data
    anomalies = data["anomalies"]

    def checkAnomalies(label):
        return label in anomalies

    def iterateAndRun(frame: np.ndarray, label: str):
        for func in listOfFunctions:
            threads = threading.Thread(
                target=lambda: func(frame, label),
                daemon=True,
            )
            threads.start()

    def code(frame: np.ndarray) -> np.ndarray:
        """
        Detect objects in the given frame
        Returns annotated frame or original frame
        """

        # Run YOLO detection
        results = model(frame)

        # Annotate the frame
        annotated_frame = results[0].plot()

        # Check for human detection
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                label = model.names[cls]

                if checkAnomalies(label) and not liveState["isAnomaly"]:
                    print(f"> {label} detected!")
                    liveState["isAnomaly"] = True
                    iterateAndRun(frame, label)

        return annotated_frame

    return code


def DoNothing(frame: np.ndarray) -> np.ndarray:
    """
    Do nothing to the frame
    Returns the original frame
    """
    return frame


def RenderFrameActions(frame: np.ndarray, actions: List[DoNothing]) -> np.ndarray:
    for action in actions:
        newframe = action(frame)
        # if (newframe is None):
        #     newframe = frame

    return newframe
