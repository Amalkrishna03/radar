import cv2

from model.vector import GetNow, SaveSituation
from model.vision import VisionModel

if __name__ == "__main__":
    frame = cv2.imread("./image.png")
    text = VisionModel(frame)

    print(text)
    SaveSituation(text, "1234567890", GetNow())
