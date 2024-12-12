import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import time

isCapturing = True


def VideoCapture(
    capture: cv2.VideoCapture,
    root: ctk.CTk,
    DetectObjects,
    videoLabel: ctk.CTkLabel,
):
    """Continuously capture and process video frames"""
    # Open webcam
    cap = capture

    def convertFrame(frame):
        """Convert OpenCV frame to CustomTkinter-compatible image"""
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = img.resize((640, 480))  # Resize for consistent display
        return ImageTk.PhotoImage(image=img)

    try:
        while isCapturing:
            # Capture frame
            ret, frame = cap.read()
            if not ret:
                break

            # Detect objects
            processedFrame = DetectObjects(frame)

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


# def create_webcam_app(objectDetector: ObjectDetectorType):
#     """
#     Create a functional webcam object detection application
#     """

#     def update_detection_button():
#         """Toggle detection and update button text"""
#         detection_state = objectDetector['toggle_detection']()
#         detect_button.configure(
#             text="Detection ON" if detection_state else "Detection OFF"
#         )

#     # Set up the UI
