import asyncio
import threading
import torch

import numpy as np
from typing import List, Callable
from ultralytics import YOLO
from utils.state import LiveState, State

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

model_name: str = "yolov8n.pt"
model = YOLO(model_name)
# model.to('cuda')

data = State.get_instance().data
anomalies = data["anomalies"]

def RunYolo(liveState: LiveState):

    def checkAnomalies(label):
        return label in anomalies

    def code(frame: np.ndarray) -> np.ndarray:
        """
        Detect objects in the given frame
        Returns annotated frame or original frame
        """

        # Run YOLO detection
        results = model(frame)
        
        # if len(results) == 0:
        #     liveState["isComparing"] = True
        #     liveState["isDetecting"] = False
        #     liveState["isAnomaly"] = False
        #     liveState["isSaving"] = False

        # Check for human detection
        for result in results:
            boxes = result.boxes
            if len(boxes) == 0:
                liveState["isComparing"] = True
                liveState["isDetecting"] = False
                liveState["isAnomaly"] = False
                liveState["isSaving"] = False
                
            flag = False
            for box in boxes:
                cls = int(box.cls[0])
                label = model.names[cls]

                if checkAnomalies(label):
                    liveState["isAnomaly"] = True
                    flag = True
                    
            if flag is False:
                liveState["isComparing"] = True
                liveState["isDetecting"] = False
                liveState["isAnomaly"] = False
                liveState["isSaving"] = False
                   

    return code

def RunYoloSimple():
    def code(frame: np.ndarray) -> np.ndarray:
        """
        Detect objects in the given frame
        Returns annotated frame or original frame
        """

        # Run YOLO detection
        results = model(frame)

        # Annotate the frame
        annotated_frame = results[0].plot()
                    
        return annotated_frame

    return code

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
                    liveState["isAnomaly"] = True
                    iterateAndRun(frame, label)

        return annotated_frame

    return code


def DoNothing(frame: np.ndarray, label: str) -> np.ndarray:
    """
    Do nothing to the frame
    Returns the original frame
    """
    print("> Anomaly Detected", label)
    return frame


def RenderFrameActions(frame: np.ndarray, actions: List[DoNothing]) -> np.ndarray:
    for action in actions:
        newframe = action(frame)
        # if (newframe is None):
        #     newframe = frame

    return newframe
