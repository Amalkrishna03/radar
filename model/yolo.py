from typing import Optional
import cv2
import numpy as np
from ultralytics import YOLO

model_name: str = 'yolov8n.pt'

def ObjectDetectionModel():
    """
    Create an object detection context with configurable state
    """
    # Closure to maintain detection state
    detection_state = {
        'active': True,
        'model': YOLO(model_name)
    }

    def setState() -> bool:
        """Toggle object detection on/off"""
        detection_state['active'] = not detection_state['active']
        return detection_state['active']

    def DetectObjects(frame: np.ndarray) -> np.ndarray:
        """
        Detect objects in the given frame
        Returns annotated frame or original frame
        """
        # If detection is not active, return original frame
        if not detection_state['active']:
            return frame

        # Run YOLO detection
        results = detection_state['model'](frame)
        
        # Annotate the frame
        annotated_frame = results[0].plot()
        
        # Check for human detection
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                if detection_state['model'].names[cls] == 'person':
                    print("Human detected!")
        
        return annotated_frame

    return {
        'setState': setState,
        'DetectObjects': DetectObjects
    }