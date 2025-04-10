import cv2
import signal
from utils.state import LiveState, State

fps = 20.0
frame_width, frame_height = 640, 480
fourcc = cv2.VideoWriter_fourcc(*"mp4v")


video_writers = []


def cleanup_handler(sig, frame):
    print("> Stopping video capture")
    for writer in video_writers:
        if writer is not None:
            writer.release()


signal.signal(signal.SIGINT, cleanup_handler)


def WriteCapture(
    capture: cv2.VideoCapture, liveState: LiveState, name="output_video.mp4"
):
    out = cv2.VideoWriter(name, fourcc, fps, (frame_width, frame_height))

    video_writers.append(out)
    print("> Saving video capture")

    try:
        while liveState["isSaving"] is True:
            ret, frame = capture.read()
            if not ret:
                break

            out.write(frame)
    finally:
        if out in video_writers:
            video_writers.remove(out)
        out.release()
        print("> Stopping video capture")
        
        liveState["isSaving"] = False
