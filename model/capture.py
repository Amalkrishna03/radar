import time

import customtkinter as ctk
import cv2

from visual.preprocessing import convertFrame
from utils.state import State


def VideoCapture(
    capture: cv2.VideoCapture,
    root: ctk.CTk,
    processFrame: callable,
    videoLabel: ctk.CTkLabel,
    state: State,
):
    """Continuously capture and process video frames"""
    # Open webcam
    cap = capture

    try:
        while True:
            # Capture frame
            ret, frame = cap.read()
            if not ret:
                break

            # Detect objects
            processedFrame = processFrame(frame) if state["isDetecting"] else frame

            # Convert and display frame
            photo = convertFrame(processedFrame)
            videoLabel.configure(image=photo)
            videoLabel.image = photo

            # Small delay to control frame rate
            time.sleep(0.025)

            # Update UI to prevent freezing
            root.update()

    except Exception as e:
        print(f"Error in video capture: {e}")
    finally:
        cap.release()
