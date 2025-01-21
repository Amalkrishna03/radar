import base64

import cv2
import numpy as np


def GetBase64(image: cv2.typing.MatLike):
    success, buffer = cv2.imencode(".png", image)

    if success:
        base64_image = base64.b64encode(buffer).decode("utf-8")
        str = f"data:image/jpeg;base64,{base64_image}"

        return base64_image, buffer.tobytes(), str

    return None


def GetBytes(image: cv2.typing.MatLike, format: str = ".png"):
    success, buffer = cv2.imencode(format, image)

    if success:
        return buffer.tobytes()

    return None


def ByteToImage(data: bytes):
    nparr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def ImageToStreamBytes(image: cv2.typing.MatLike):
    frame_bytes = GetBytes(image, ".jpg")

    if frame_bytes:
        return b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"

    return None
