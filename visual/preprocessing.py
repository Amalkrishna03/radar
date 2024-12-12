import cv2

threshold = 30
# if 1, small changes will be detected easily


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
