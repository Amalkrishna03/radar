import cv2
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from server import app
from visual.image import ImageToStreamBytes

isStreaming = True


@app.get("/start_stream")
async def start_stream():
    global isStreaming
    isStreaming = True
    return {"status": "started"}


@app.get("/stop_stream")
async def stop_stream():
    global isStreaming
    isStreaming = False
    return {"status": "stopped"}


def main(capture: cv2.VideoCapture):
    print("Starting stream")

    def generate_frames():
        global isStreaming
        while isStreaming:
            success, frame = capture.read()
            if success:
                streamData = ImageToStreamBytes(frame)
                if streamData:
                    yield streamData

    @app.get("/video_feed")
    async def video_feed():
        return StreamingResponse(
            generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame"
        )

    # @app.lifespan("shutdown")
    # async def shutdown_event():
    #     if capture.isOpened():
    #         capture.release()

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    templates = Jinja2Templates(directory="templates")

    @app.get("/", response_class=HTMLResponse)
    async def root(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    capture = cv2.VideoCapture(0)
    if not capture.isOpened():
        raise IOError("Cannot open webcam")

    main(capture)

# uv run stream.py
