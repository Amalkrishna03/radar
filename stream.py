import cv2
import uvicorn
from fastapi.responses import StreamingResponse

from server import app
from visual.image import ImageToStreamBytes

isStreaming = True


@app.get("/live/start_stream")
async def start_stream():
    global isStreaming
    isStreaming = True
    return {"status": "started"}


@app.get("/live/stop_stream")
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

    @app.get("/live/stream")
    async def video_feed():
        return StreamingResponse(
            generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame"
        )

    # @app.lifespan("/live/shutdown")
    # async def shutdown_event():
    #     if capture.isOpened():
    #         capture.release()

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    capture = cv2.VideoCapture(0)
    if not capture.isOpened():
        raise IOError("Cannot open webcam")

    main(capture)

# uv run stream.py
