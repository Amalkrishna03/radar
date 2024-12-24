from typing import TypedDict, TypeVar, Generic
import json
import os

defaultState = {
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
def load_state():
    if os.path.exists("state.json"):
        with open("state.json", "r") as file:
            state = json.load(file)
            
            return state
        
    return defaultState

T = TypeVar('T')

class Priority(Generic[T]):
    high: T
    medium: T
    low: T

class State(TypedDict):
    priority: Priority[tuple[int, int, int, int]]
    interval: int
    priorityThreshold: Priority[int]
    
class LiveState(TypedDict):
    initial: list
    something: list
    isCapturing: bool
    isDetecting: bool
    isComparing: bool
    isSaving: bool
