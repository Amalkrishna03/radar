from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
import cv2
import uvicorn
from typing import Generator
import numpy as np

app = FastAPI()

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)  # 0 is usually the built-in webcam
        if not self.cap.isOpened():
            raise RuntimeError("Could not start camera.")

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

    def get_frame(self) -> bytes:
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        # Encode the frame in JPEG format
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

def generate_frames(camera: Camera) -> Generator[bytes, None, None]:
    while True:
        frame = camera.get_frame()
        if frame is None:
            break
            
        # Yield the frame in multipart format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Create a single camera instance
camera = Camera()

@app.get("/")
async def index():
    return Response(content="""
        <html>
            <head>
                <title>Webcam Stream</title>
            </head>
            <body>
                <h1>Live Webcam Stream</h1>
                <img src="/video_feed" width="640" height="480" />
            </body>
        </html>
    """, media_type="text/html")

@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(
        generate_frames(camera),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

# if __name__ == "__main__":
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)