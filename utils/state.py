from typing import TypedDict, Literal

state = {
    "isCapturing": True,
    "isDetecting": True,
    "isComparing": True,
    "priority": {
        "high": (200, 200, 400, 300),
        "medium": (100, 100, 200, 150),
    },
    "interval": 1,
    "priorityThreshold": {
        "high": 10,
        "medium": 20,
        "low": 30,
    }
}


class State(TypedDict):
    isCapturing: bool
    isDetecting: bool
    isComparing: bool
    priority: dict[str, tuple[int, int, int, int]]
    interval: int
    priorityThreshold: dict[str, int]