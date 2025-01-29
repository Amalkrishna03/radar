from functools import reduce
import customtkinter as ctk

import cv2
import numpy as np

from PIL import Image, ImageTk
from utils.state import StateType

flip = False
threshold = 30
# if 1, small changes will be detected easily

width = 640 * 2
height = 480 * 2


def convertFrame(frame):
    """Convert OpenCV frame to CustomTkinter-compatible image"""
    frame = cv2.cvtColor(cv2.flip(frame, 1) if flip else frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    img = img.resize((width, height))  # Resize for consistent display

    return ImageTk.PhotoImage(image=img)


def PreprocessFrame(frame: cv2.typing.MatLike):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gray_blurred = cv2.GaussianBlur(gray, (21, 21), 0)

    return gray


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


def ExtractPriorityOld(frame: cv2.typing.MatLike, coordinates: tuple):  # type: ignore
    x, y, w, h = coordinates

    low = frame.copy()

    cv2.rectangle(low, (x, y), (x + w, y + h), color, -1)

    high = frame[y : y + h, x : x + w]

    return low, high

def ExtractPriority(frame: cv2.typing.MatLike, points: np.ndarray):
    low = frame.copy()
    
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    cv2.fillPoly(mask, [points], 255)
    mask_inv = cv2.bitwise_not(mask)
    
    low = cv2.bitwise_and(low, low, mask=mask_inv)
    
    x, y, w, h = cv2.boundingRect(points)
    
    padding = 10
    x = max(0, x - padding)
    y = max(0, y - padding)
    w = min(frame.shape[1] - x, w + 2 * padding)
    h = min(frame.shape[0] - y, h + 2 * padding)
    
    high = cv2.bitwise_and(frame, frame, mask=mask)
    cropped_high = high[y:y+h, x:x+w]
    
    # cv2.imshow('Modified Frame (Full)', low)
    # cv2.imshow('Extracted Region (Cropped)', cropped_high)
    # cv2.waitKey(0)
    
    return low, cropped_high


def DrawRectangles(
    frame: ctk.CTkFrame, rectangle: tuple, color=(0, 255, 0), thickness=1
):
    """
    Draw rectangles on the input frame

    Args:
        frame (numpy.ndarray): Input image frame
        rectangles (tuple): rectangle coordinates
                           (x1, y1, x2, y2)

    Returns:
        numpy.ndarray: Frame with rectangles drawn
    """
    return cv2.rectangle(
        frame.copy(),
        (rectangle[0], rectangle[1]),  # Top-left corner
        (rectangle[2], rectangle[3]),  # Bottom-right corner
        color,
        thickness,
    )


def DrawPolygon(frame: ctk.CTkFrame, points: np.ndarray, color=(0, 255, 0), thickness=1):
    """
    Draw a polygon on the input frame using a list of points
    Args:
        frame (numpy.ndarray): Input image frame
        points (list): List of [x,y] coordinates forming the polygon
                      Example: [[x1,y1], [x2,y2], [x3,y3], ...]
        color (tuple): RGB color for the polygon outline (default: green)
        thickness (int): Line thickness for the polygon outline (default: 1)
    Returns:
        numpy.ndarray: Frame with polygon drawn
    """
    
    return cv2.polylines(
        frame,
        [points],
        isClosed=True,  
        color=color,
        thickness=thickness,
    )


def DrawWrapped(data):
    priority = data["priority"]
    oldpriority = data["oldpriority"]
    def code(frame: ctk.CTkFrame):
        fh = DrawPolygon(frame, priority["high"], color=(0, 0, 255))
        fm = DrawPolygon(fh, priority["medium"], color=(0, 255, 0))
        
        # oh = DrawRectangles(fm, oldpriority["high"], color=(0, 0, 255))
        # om = DrawRectangles(oh, oldpriority["medium"], color=(0, 255, 0))
        # return om
        
        return fm


    return code
