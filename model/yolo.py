from typing import Optional
import cv2
import numpy as np
from ultralytics import YOLO

model_name: str = "yolov8n.pt"
model = YOLO(model_name)


def DetectObjects(frame: np.ndarray) -> np.ndarray:
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
            if model.names[cls] == "person":
                print("Human detected!")

    return annotated_frame

def DoNothing(frame: np.ndarray) -> np.ndarray:
    """
    Do nothing to the frame
    Returns the original frame
    """
    return frame
    