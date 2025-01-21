import cv2
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.routing import APIRoute
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware

from api.main import api_router
from visual.image import ImageToStreamBytes

app = FastAPI(title="RADAR")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


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

    @app.lifespan("shutdown")
    async def shutdown_event():
        if capture.isOpened():
            capture.release()

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    capture = cv2.VideoCapture(0)
    if not capture.isOpened():
        raise IOError("Cannot open webcam")

    main(capture)
