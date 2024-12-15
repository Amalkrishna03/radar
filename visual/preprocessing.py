from functools import reduce

import cv2
from PIL import Image, ImageTk
from utils.state import State


threshold = 30
# if 1, small changes will be detected easily

def convertFrame(frame):
    """Convert OpenCV frame to CustomTkinter-compatible image"""
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    img = img.resize((640, 480))  # Resize for consistent display
    return ImageTk.PhotoImage(image=img)


def PreprocessFrame(frame: cv2.typing.MatLike):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.GaussianBlur(gray, (21, 21), 0)

    return gray_blurred


def FindVisualDifference(
    frame1: cv2.typing.MatLike, frame2: cv2.typing.MatLike, threshold: int = threshold
):
    diff = cv2.absdiff(frame1, frame2)
    _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

    total_pixels = thresh.size
    changed_pixels = cv2.countNonZero(thresh)
    change_percentage = (changed_pixels / total_pixels) * 100

    return change_percentage


color = (0, 0, 0)
def ExtractPriority(frame: cv2.typing.MatLike, coordinates: tuple):  # type: ignore
    x, y, w, h = coordinates

    low = frame.copy()

    cv2.rectangle(low, (x, y), (x + w, y + h), color, -1)

    high = frame[y : y + h, x : x + w]

    return low, high

def DrawRectangles(frame, rectangles):
    """
    Draw rectangles on the frame using functional approach.
    
    Args:
        frame (numpy.ndarray): Input image frame
        rectangles (list): List of rectangle coordinates 
                           [(x1, y1, x2, y2), ...]
    
    Returns:
        numpy.ndarray: Frame with rectangles drawn
    """
    return reduce(
        lambda img, rect: cv2.rectangle(
            img, 
            (rect[0], rect[1]),  # Top-left corner
            (rect[2], rect[3]),  # Bottom-right corner
            (0, 255, 0),  # Green color
            2  # Line thickness
        ),
        rectangles,
        frame.copy()  # Start with a copy of the original frame
    )
    
def DrawWrapped(data:State):
    return lambda frame: DrawRectangles(frame, data["priority"].values())