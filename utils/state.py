from typing import TypedDict, TypeVar, Generic
import json
import os

from utils.canvas import load_canvas

defaultState = {
    "oldpriority": {
        "high": (200, 200, 400, 300),
        "medium": (100, 100, 200, 150),
    },
    "interval": 1,
    "priorityThreshold": {
        "high": 10,
        "medium": 20,
        "low": 30,
    },
    "anomalies": [
        "person",
        "car",
    ],
}

def load_state():
    print("> Loading state file")
    if os.path.exists("state.json"):
        with open("state.json", "r") as file:
            state = json.load(file)
            
            requiredKeys = defaultState.keys()
            
            for key in requiredKeys:
                if key not in state:
                    print(f"> Missing key {key} in state file")
                    state[key] = defaultState[key]
                    
            return state
            

    else:
        print("> State file not found")
        return defaultState

class State:
    _instance = None

    def _init_(self, state_data=None, canvas_data=None):
        self.data
        self.data["priority"]

    @classmethod
    def get_instance(cls, state_data=None, canvas_data=None):
        if cls._instance is None:
            cls._instance = State()
            
        if state_data is not None:
            cls._instance.data = state_data
            
        if canvas_data is not None:
            cls._instance.data["priority"] = canvas_data
            
        return cls._instance

initialState = State.get_instance(load_state(), load_canvas())


T = TypeVar("T")


class Priority(Generic[T]):
    high: T
    medium: T
    low: T


class StateType(TypedDict):
    priority: Priority[tuple[int, int, int, int]]
    interval: int
    priorityThreshold: Priority[int]
    annomalies: list


class LiveState(TypedDict):
    initial: list
    something: list
    isCapturing: bool
    isDetecting: bool
    isComparing: bool
    isAnomaly: bool
    isSaving: bool

if __name__ == "__main__":
    print(initialState.data)