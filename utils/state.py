from typing import TypedDict, Literal, TypeVar, Generic

state = {
    "isCapturing": True,
    "isDetecting": False,
    "isComparing": True,
    "isSaving": False,
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

T = TypeVar('T')

class Priority(Generic[T]):
    high: T
    medium: T
    low: T

class State(TypedDict):
    isCapturing: bool
    isDetecting: bool
    isComparing: bool
    isSaving: bool
    priority: Priority[tuple[int, int, int, int]]
    interval: int
    priorityThreshold: Priority[int]